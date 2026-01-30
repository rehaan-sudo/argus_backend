# Import all models to ensure SQLAlchemy registers their Table metadata
from . import (
    alert_log, attendance, branch, bus, bus_onboard_summary, camera_log, camera,
    city, defect_log, employee, group, inventory_item, loyalty_member, machine,
    machine_status_log, ml_feature, ml_inference_run, ml_model, ml_prediction,
    organization, ppe_violation, production_log, role, safety_record, stock_alert,
    sub_group, user, user_settings, video_session, violation_by_gear, visit,
    visitor, vpn_config
)

# Expose Base for convenience

from .base import Base

from .user import User
from .user_settings import UserSettings
from .audit import Audit
from .city import City
from .branch import Branch

from .usecase import InfoUseCase
from .stamping import InfoUseCaseStamping
# Import all models to ensure SQLAlchemy registers their Table metadata
from . import (
    alert_log, attendance, branch, bus, bus_onboard_summary, camera_log, camera,
    city, defect_log, employee, group, inventory_item, loyalty_member, machine,
    machine_status_log, ml_feature, ml_inference_run, ml_model, ml_prediction,
    organization, ppe_violation, production_log, role, safety_record, stock_alert,
    sub_group, user, user_settings, video_session, violation_by_gear, visit,
    visitor, vpn_config
)

# Base
from .base import Base

# Core models
from .user import User
from .user_settings import UserSettings
from .audit import Audit
from .city import City
from .branch import Branch
from .camera import Camera

# Use case masters
from .usecase import InfoUseCase
from .stamping import InfoUseCaseStamping

# User onboarding flow
from .user_usecase import UserUseCase
from .user_stamping_usecase import UserStampingUseCase  


from .user_usecase import UserUseCase


from .camera import Camera
