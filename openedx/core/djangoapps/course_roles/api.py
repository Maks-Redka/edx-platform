"""
Helpers for the course roles app.
"""
from __future__ import annotations

from django.contrib.auth.models import AnonymousUser, User  # lint-amnesty, pylint: disable=imported-auth-user
from django.db.models import Q
from opaque_keys.edx.keys import CourseKey

from edx_django_utils.cache import RequestCache
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.core.djangoapps.course_roles.models import UserRole
from openedx.core.djangoapps.course_roles.data import CourseRolesPermission


def get_all_user_permissions_for_a_course(
    user: User | AnonymousUser, course_key: CourseKey
) -> set[CourseRolesPermission]:
    """
    Get all of a user's permissions for a course,
    including, if applicable, organization-wide permissions
    and instance-wide permissions.
    """
    if isinstance(user, AnonymousUser):
        return set()
    if not isinstance(course_key, CourseKey):
        raise TypeError('course_key must be a CourseKey')
    if not isinstance(user, User):
        raise TypeError('user must be a User')
    cache = RequestCache("course_roles")
    cache_key = f"all_user_permissions_for_course:{user.id}:{course_key}"
    cached_response = cache.get_cached_response(cache_key)
    if cached_response.is_found:
        return cached_response.value
    if not CourseOverview.course_exists(course_key):
        raise ValueError('course does not exist')
    permissions_qset = UserRole.objects.filter(
        Q(user=user),
        (
            # Course-specific roles
            Q(course=course_key) |
            # Org-wide roles that apply to this course
            (Q(course__isnull=True) & Q(org__name=course_key.org)) |
            # Instance-wide roles
            Q(org__isnull=True)
        )
    )
    permissions = set(
        CourseRolesPermission[permission_name.upper()]
        for permission_name
        in permissions_qset.values_list('role__permissions__name', flat=True)
    )
    cache.set(cache_key, permissions)

    return permissions
