import attr
from pygments.lexers.python import Python3Lexer
from typing import List

from ..core.core_settings import app_settings
from ..exporters import *
from ..model.app_data import ApiCall


def to_python_requests(idx, api_call, last_exchange):
    func_name = get_function_name(api_call)
    method = last_exchange.request.http_method
    url = last_exchange.request.http_url
    has_qp = True if last_exchange.request.query_params else False
    query_params = dict_formatter(
        last_exchange.request.query_params.items(),
        "\"{k}\": \"{v}\""
    )
    has_headers = True if last_exchange.request.headers else False
    headers = dict_formatter(
        last_exchange.request.headers.items(),
        "\"{k}\": \"{v}\"",
        splitter=",\n"
    )
    has_json_body = True if last_exchange.request.request_body else False

    json_body = "data=\"{}\"".format(
        encode_json_string(last_exchange.request.request_body) if has_json_body else "")

    params_code = f"""
    params={{
        {query_params if has_qp else ""}
    }},
    """

    headers_code = f"""
    headers={{
        {headers if has_headers else ""}
    }},
    """
    py_func = f"""
    @seq_task({idx + 1})
    # @task(10) # To run this test 10 times
    def {func_name}(self):
        # Group requests if it contains variable params
        # self.client.get("/api?id=%i" % i, name="/api?id=[id]")
        response = self.client.{method.lower()}(
                "{url}",
                {params_code if has_qp else ""}
                {headers_code if has_headers else ""}
                {json_body if has_json_body else ""}
        )
        print(f'Response HTTP Status Code: {{response.status_code}}')
    """
    return py_func


@attr.s
class LocustTestsExporter:
    name: str = "Locust (Performance Tests)"
    output_ext: str = "py"

    def export_data(self, api_calls: List[ApiCall]):
        file_header = """
# python3 -m pip install locustio - See https://docs.locust.io/en/stable/installation.html
# Running the tests
# locust -f this_file.py
# For improving performance
# Install - python3 -m pip install geventhttpclient
# Then use FastHttpLocust instead of HttpLocust

from locust import HttpLocust, TaskSet, TaskSequence
import json
import random
import string
import uuid

def random_uuid():
    return str(uuid.uuid4())
    
def random_str(length=10, with_punctuation=False):
    selection = string.ascii_letters + string.digits
    selection = selection + string.punctuation if with_punctuation else selection
    return ''.join(random.choice(selection) for i in range(length))
    
def random_int(min=0, max=100):
    return random.randint(min, max)
    
class ApiBehaviour(TaskSequence):
        """
        file_footer = """
class ApiUser(HttpLocust):
    task_set = ApiBehavior
    host = "localhost"
        
        """
        output = [
            self.__export_api_call(idx, api_call)
            for idx, api_call in enumerate(api_calls)
        ]
        unformatted_code = file_header + "\n".join(output) + file_footer
        formatted_code, _ = format_python_code(unformatted_code)

        return highlight(formatted_code, Python3Lexer(), HtmlFormatter())

    def __export_api_call(self, idx, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        doc = f"""
    # {api_call.title}
    {to_python_requests(idx, api_call, last_exchange)}
"""
        return doc


exporter = LocustTestsExporter()
