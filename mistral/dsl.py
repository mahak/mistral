# -*- coding: utf-8 -*-
#
# Copyright 2013 - Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import yaml
from yaml import error


class Parser(object):
    """Mistral DSL parser.

    Loads a workbook definition in YAML format as described in Mistral DSL
    specification and provides various methods to access DSL entities like
    tasks and actions in a form of dictionary.
    """
    def __init__(self, workbook_definition):
        try:
            self.doc = yaml.safe_load(workbook_definition)
        except error.YAMLError as exc:
            raise RuntimeError("Definition could not be parsed: %s\n"
                               % exc.message)

    def get_services(self):
        services = []
        for service_name in self.doc.get("Services", []):
            services.append(self.doc["Services"][service_name])
        return services

    def get_service(self, service_name):
        return self.doc["Services"].get(service_name, {})

    def get_events(self):
        events_from_doc = self.doc["Workflow"].get("events", None)
        if not events_from_doc:
            return []
        events = []
        for name in events_from_doc:
            event_dict = {'name': name}
            event_dict.update(events_from_doc[name])
            events.append(event_dict)
        return events

    def get_tasks(self):
        tasks = self.doc.get("Workflow", {}).get("tasks", {})

        for task_name, task_dsl in tasks.iteritems():
            task_dsl["service_name"] = task_dsl["action"].split(':')[0]
            req = task_dsl.get("requires")
            if req and isinstance(req, list):
                task_dsl["requires"] = dict(zip(req, ['']*len(req)))

        return tasks

    def get_task(self, task_name):
        return self.get_tasks().get(task_name, {})

    def get_task_dsl_property(self, task_name, property_name):
        task_dsl = self.get_task(task_name)
        return task_dsl.get(property_name)

    def get_task_on_error(self, task_name):
        return self.get_task_dsl_property(task_name, "OnError")

    def get_task_on_success(self, task_name):
        return self.get_task_dsl_property(task_name, "OnSuccess")

    def get_task_input(self, task_name):
        return self.get_task_dsl_property(task_name, "input")

    def get_action(self, task_action_name):
        if task_action_name.find(":") == -1:
            return {}
        service_name = task_action_name.split(':')[0]
        action_name = task_action_name.split(':')[1]
        action = self.get_service(service_name)['actions'][action_name]
        return action

    def get_actions(self, service_name):
        service = self.get_service(service_name)
        return service.get('actions', [])

    def get_service_names(self):
        names = []
        for name in self.doc['Services']:
            names.append(name)
        return names

    def get_event_task_name(self, event_name):
        event = self.doc["Workflow"]["events"].get(event_name)
        return event.get('tasks') if event else ""