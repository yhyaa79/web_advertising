from django import template
from django.template.loader import render_to_string

from listings.category_config import (
    get_main_category,
    get_listing_card_private_fields,
    listing_card_masks_image,
    listing_card_show_image,
)

register = template.Library()


@register.filter
def listing_main_category(listing):
    return get_main_category(getattr(listing, "category", None) or "") or "other"


@register.simple_tag(takes_context=True)
def sensitive_class(context, listing, field_key):
    """CSS class for private listings when viewer lacks approved access."""
    if not getattr(listing, "is_private", False):
        return ""
    request = context.get("request")
    user = request.user if request else context.get("user")
    user_key = getattr(user, "pk", None) if getattr(user, "is_authenticated", False) else None
    access_cache = getattr(listing, "_listing_card_access_cache", {})
    if user_key not in access_cache:
        access_cache[user_key] = listing.has_access(user)
        listing._listing_card_access_cache = access_cache
    if access_cache[user_key]:
        return ""
    main = get_main_category(getattr(listing, "category", None) or "") or "other"
    if field_key == "image":
        return "listing-sensitive listing-sensitive--image" if listing_card_masks_image(main) else ""
    fields = get_listing_card_private_fields(main)
    if field_key in fields:
        return "listing-sensitive listing-sensitive--chess"
    return ""


@register.simple_tag(takes_context=True)
def render_listing_card(context, listing, promoted=False):
    main = get_main_category(getattr(listing, "category", None) or "") or "other"
    template_names = [
        f"listings/partials/cards/{main}.html",
        "listings/partials/cards/other.html",
    ]
    ctx = {
        **context.flatten(),
        "listing": listing,
        "promoted": promoted,
        "card_main": main,
        "card_show_image": listing_card_show_image(main),
    }
    return render_to_string(template_names, ctx, request=context.get("request"))
