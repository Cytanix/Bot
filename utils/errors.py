# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""This file contains all the errors that can be raised"""
from aiohttp.web_exceptions import HTTPUnauthorized

class InvalidEndpointError(ValueError):
    """Error that is raised when an invalid endpoint is requested from the API"""
    def __init__(self, endpoint):
        super().__init__(f"Invalid endpoint {endpoint}")

class NSFWEndpointCalled(Exception):
    """Error that is raised when an NSFW endpoint is requested from the API"""
    def __init__(self):
        super().__init__(f"NSFW endpoints have been disabled for this guild. "
                         f"If you feel this is a mistake, please contact SpiritTheWalf")

class UnauthorizedError(HTTPUnauthorized):
    """Error that is raised when an unauthorized request is made to the API"""
    def __init__(self):
        super().__init__(reason="Unauthorized, please make sure your API key is correct.")