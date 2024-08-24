from django.views.decorators.http import require_http_methods
from django.template import TemplateDoesNotExist
from django.shortcuts import redirect, render
from django.http import Http404
from django.urls import reverse
from . import forms
from . import util
import random


def render_page(request, template, context=None):
    try:
        template_name = f"encyclopedia/{template}.html"
        return render(request, template_name, context)

    except TemplateDoesNotExist:
        raise Http404()


def redirect_to_entry_page(title):
    return redirect(reverse("encyclopedia:entry", kwargs={"title": title}))


def handle_form_errors(request, form, error_message, template, context=None):
    context = context or {}
    form.add_error(None, error_message)
    context["form"] = form
    return render_page(request, template, context)


def handle_form_submission(request, template, context=None, is_edit=False):
    try:
        form = forms.EntryForm(request.POST)

        if not form.is_valid():
            error_message = "Please make sure to fill out all fields. Each field is required to complete the form."
            return handle_form_errors(request, form, error_message, template, context)

        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        entry_exists = util.get_entry(title)

        if not is_edit and entry_exists:
            error_message = "An entry with this title already exists. Please choose a different title."
            return handle_form_errors(request, form, error_message, template, context)

        util.save_entry(title, content)
        return redirect_to_entry_page(title)

    except UnicodeDecodeError:
        error_message = "Something went wrong while processing the content. Please check that the text is in the correct format and try again."
        return handle_form_errors(request, form, error_message, template, context)


@require_http_methods(["GET"])
def index(request):
    return render_page(request, "index", {"entries": util.list_entries()})


@require_http_methods(["GET"])
def entry_page(request, title):
    html_content = util.convert_markdown_to_html(title)
    if not html_content:
        raise Http404()

    return render_page(request, "entry", {"title": title, "content": html_content})


@require_http_methods(["GET"])
def search(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return redirect(reverse("encyclopedia:index"))

    entries = util.list_entries()
    lowercase_query = util.str_lower(query)
    entries_dict = {util.str_lower(entry): entry for entry in entries}

    if lowercase_query in entries_dict:
        return redirect_to_entry_page(entries_dict[lowercase_query])

    matching_entries = util.find_matching_entries(entries, lowercase_query)
    return render_page(request, "search", {"entries": matching_entries, "query": query})


@require_http_methods(["GET", "POST"])
def new_entry(request):
    if request.method != "POST":
        return render_page(
            request, "new", {"form": forms.EntryForm(hidden_title=False)}
        )

    return handle_form_submission(request, "new")


@require_http_methods(["GET", "POST"])
def edit_entry(request, title):
    content = util.get_entry(title)
    if not content:
        raise Http404()

    if request.method != "POST":
        return render_page(request, "edit", {
                "form": forms.EntryForm(initial={"title": title, "content": content}, hidden_title=True),
                "title": title,
            },
        )

    context = {"title": title}
    return handle_form_submission(request, "edit", context, is_edit=True)


@require_http_methods(["GET"])
def random_entry(request):
    entries = util.list_entries()
    if not entries:
        raise Http404()

    entry = random.choice(entries)
    return redirect_to_entry_page(entry)


@require_http_methods(["GET"])
def handler404(request, exception=None):
    return render_page(request, "page-not-found")
