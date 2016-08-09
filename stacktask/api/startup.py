from django.apps import AppConfig
from django.conf import settings
from stacktask.exceptions import ActionNotFound, TaskViewNotFound


def check_expected_taskviews():
    expected_taskviews = settings.ACTIVE_TASKVIEWS

    missing_taskviews = list(
        set(expected_taskviews) - set(settings.TASKVIEW_CLASSES.keys()))

    if missing_taskviews:
        raise TaskViewNotFound(
            message=(
                "Expected taskviews are unregistered: %s" % missing_taskviews))


def check_expected_actions():
    """Check that all the expected actions have been registered."""
    expected_actions = []

    for taskview in settings.ACTIVE_TASKVIEWS:
        task_class = settings.TASKVIEW_CLASSES.get(taskview)['class']

        try:
            expected_actions += settings.TASK_SETTINGS.get(
                task_class.task_type, {})['default_actions']
        except KeyError:
            expected_actions += task_class.default_actions
        expected_actions += settings.TASK_SETTINGS.get(
            task_class.task_type, {}).get('additional_actions', [])

    missing_actions = list(
        set(expected_actions) - set(settings.ACTION_CLASSES.keys()))

    if missing_actions:
        raise ActionNotFound(
            "Expected actions are unregistered: %s" % missing_actions)


class APIConfig(AppConfig):
    name = 'stacktask.api'

    def ready(self):
        """A pre-startup function for the api.

        Code run here will occur before the API is up and active but after
        all models have been loaded.

        Useful for any start up checks.

        """

        # First check that all expect taskviews are present
        check_expected_taskviews()

        # Now check if all the actions those views expecte are present.
        check_expected_actions()
