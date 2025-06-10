"""
Initializer file for validation_templates/ folder.

This file enables constructions like:
`import config.validation_templates as templates`

For documentation on the specific templates, see the individual files.
"""

from config.validation_templates.environment_template import ENVIRONMENT_TEMPLATE
from config.validation_templates.plane_template import PLANE_TEMPLATE
from config.validation_templates.target_template import TARGET_TEMPLATE

__all__ = ["ENVIRONMENT_TEMPLATE", "PLANE_TEMPLATE", "TARGET_TEMPLATE"]
