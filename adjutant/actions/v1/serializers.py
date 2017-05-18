# Copyright (C) 2015 Catalyst IT Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from rest_framework import serializers
from django.conf import settings
from adjutant.actions import user_store


role_options = settings.DEFAULT_ACTION_SETTINGS.get("NewUserAction", {}).get(
    "allowed_roles", [])


def get_region_choices():
    id_manager = user_store.IdentityManager()
    return (region.id for region in id_manager.list_regions())


class BaseUserNameSerializer(serializers.Serializer):
    """
    A serializer where the user is identified by username/email.
    """
    domain_id = serializers.CharField(max_length=64, default='default')
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        super(BaseUserNameSerializer, self).__init__(*args, **kwargs)

        if settings.USERNAME_IS_EMAIL:
            self.fields.pop('username')


class BaseUserIdSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=64)


class NewUserSerializer(BaseUserNameSerializer):
    roles = serializers.MultipleChoiceField(choices=role_options)
    project_id = serializers.CharField(max_length=64)


class NewProjectSerializer(serializers.Serializer):
    parent_id = serializers.CharField(
        max_length=64, default=None, allow_null=True)
    project_name = serializers.CharField(max_length=64)
    domain_id = serializers.CharField(max_length=64, default='default')


class NewProjectWithUserSerializer(BaseUserNameSerializer):
    parent_id = serializers.CharField(
        max_length=64, default=None, allow_null=True)
    project_name = serializers.CharField(max_length=64)


class ResetUserSerializer(BaseUserNameSerializer):
    domain_name = serializers.CharField(max_length=64, default='Default')
    # override domain_id so serializer doesn't set it up.
    domain_id = None


class EditUserRolesSerializer(BaseUserIdSerializer):
    roles = serializers.MultipleChoiceField(choices=role_options)
    remove = serializers.BooleanField(default=False)
    project_id = serializers.CharField(max_length=64)
    domain_id = serializers.CharField(max_length=64, default='default')


class NewDefaultNetworkSerializer(serializers.Serializer):
    setup_network = serializers.BooleanField(default=True)
    project_id = serializers.CharField(max_length=64)
    region = serializers.CharField(max_length=100)


class NewProjectDefaultNetworkSerializer(serializers.Serializer):
    setup_network = serializers.BooleanField(default=False)
    region = serializers.CharField(max_length=100)


class AddDefaultUsersToProjectSerializer(serializers.Serializer):
    domain_id = serializers.CharField(max_length=64, default='default')


class SetProjectQuotaSerializer(serializers.Serializer):
    pass


class SendAdditionalEmailSerializer(serializers.Serializer):
    pass


class UpdateUserEmailSerializer(BaseUserIdSerializer):
    new_email = serializers.EmailField()


class UpdateProjectQuotasSerializer(serializers.Serializer):
    project_id = serializers.CharField(max_length=64)
    size = serializers.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(UpdateProjectQuotasSerializer, self).__init__(*args, **kwargs)
        # NOTE(amelia): This overide is mostly in use so that it can be tested
        # However it does take into account the improbable edge case that the
        # regions have changed since the server was last started
        self.fields['regions'] = serializers.MultipleChoiceField(
            choices=get_region_choices())

    def validate_size(self, value):
        """
        Check that the size exists in the conf.
        """
        size_list = settings.PROJECT_QUOTA_SIZES.keys()
        if value not in size_list:
            raise serializers.ValidationError("Quota size: %s is not valid"
                                              % value)
        return value
