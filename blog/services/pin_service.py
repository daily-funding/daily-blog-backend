from django.db import IntegrityError, transaction
from django.db.models import F, Max

from blog.models import Pin

MAX_PIN_COUNT = 12


class PinError(Exception):
    pass


class AlreadyPinnedError(PinError):
    pass


class PinLimitExceededError(PinError):
    pass


class NotPinnedError(PinError):
    pass


class InvalidPinOrderError(PinError):
    pass


@transaction.atomic
def add_pin(post):
    # 빈 Pin 상태에서 전역 직렬화가 보장되지 않는다.  추후 다중 관리자 동시 사용 가능성이 커지면 별도 락 row 또는 DB 제약 강화 방향필요
    pinned_qs = Pin.objects.select_for_update().order_by("sort_order")

    if pinned_qs.filter(post=post).exists():
        raise AlreadyPinnedError()

    current_count = pinned_qs.count()
    if current_count >= MAX_PIN_COUNT:
        raise PinLimitExceededError()

    last_sort_order = pinned_qs.aggregate(max_sort=Max("sort_order"))["max_sort"] or 0

    try:
        Pin.objects.create(post=post, sort_order=last_sort_order + 1)
    except IntegrityError:
        raise AlreadyPinnedError()


@transaction.atomic
def remove_pin(post):
    pinned_qs = Pin.objects.select_for_update().order_by("sort_order")

    try:
        pin = pinned_qs.get(post=post)
    except Pin.DoesNotExist:
        raise NotPinnedError()

    deleted_order = pin.sort_order
    pin.delete()

    Pin.objects.filter(sort_order__gt=deleted_order).update(
        sort_order=F("sort_order") - 1
    )


@transaction.atomic
def reorder_pins(post_ids: list[int]):
    if not post_ids:
        pinned_exists = Pin.objects.exists()
        if pinned_exists:
            raise InvalidPinOrderError()
        return

    if len(post_ids) != len(set(post_ids)):
        raise InvalidPinOrderError()

    pins = list(
        Pin.objects.select_for_update().select_related("post").order_by("sort_order")
    )

    pinned_ids = [pin.post_id for pin in pins]
    if set(post_ids) != set(pinned_ids):
        raise InvalidPinOrderError()

    pin_map = {pin.post_id: pin for pin in pins}

    update_targets = []
    for index, post_id in enumerate(post_ids, start=1):
        pin = pin_map[post_id]
        if pin.sort_order != index:
            pin.sort_order = index
            update_targets.append(pin)

    if update_targets:
        Pin.objects.bulk_update(update_targets, ["sort_order"])
