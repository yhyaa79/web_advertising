"""Prefetch helpers for listing list cards."""

LISTING_CARD_PREFETCH = (
    "website_details",
    "ecommerce_details",
    "app_details",
    "social_details",
    "content_details",
    "domain_details",
    "service_details",
)


def prefetch_listing_card_details(queryset):
    return queryset.prefetch_related(*LISTING_CARD_PREFETCH)
