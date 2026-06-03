# -*- coding: utf-8 -*-
from testbase.conf import settings
import time
import jpype
from tcmpp_saas_autotest.tcmpp_autotestcase.open_api.app_manage_api.utils.open_api_app_function_utils import (
    OpenApiAppFunctionUtils)
from tcmpp_saas_autotest.tcmpp_autotestcase.open_api.mini_game_manage_api.utils.open_api_mini_game_function_utils import OpenApiMngGameFunctionUtils
from tcmpp_saas_autotest.tcmpp_autotestcase.open_api.team_manage_api.utils.open_api_team_function_utils import OpenApiTeamFunctionUtils
from tcmpp_saas_autotest.tcmpp_autotestlib.tcmpp_api_testbase import TcmppSaaSAutotestTestCase
from tcmpp_saas_autotest.tcmpp_autotestlib.app.tcmpp_app_api_lib import AppApiRequestData, AppApiResponseStructure
from tcmpp_saas_autotest.tcmpp_autotestlib.app.tcmpp_app_api_utils import AppApiUtils


class CoreProcessTestcase(TcmppSaaSAutotestTestCase):
    """
    OpenApi：核心流程测试用例，创建小游戏版本、提交上架审核、上架审核通过、发布小游戏、客户端拉取小游戏成功
    """
    owner = "jadengeng"
    timeout = 5
    priority = TcmppSaaSAutotestTestCase.EnumPriority.High
    status = TcmppSaaSAutotestTestCase.EnumStatus.Ready
    tags = "function"

    def run_test(self):

        self.start_step("根据小游戏名称查询小游戏mng_id")
        mng_id = OpenApiMngGameFunctionUtils.query_mng_by_name(self, settings.TCMPP_MNG_NAME)

        self.start_step("获取团队的id")
        mini_team_id = OpenApiTeamFunctionUtils.get_team_id(self, settings.TCMPP_MINI_TEAM)
        app_team_id = OpenApiTeamFunctionUtils.get_team_id(self, settings.TCMPP_APP_TEAM)

        self.start_step("查询当前账号的应用ID")
        application_id = OpenApiAppFunctionUtils.get_application_id(self)

        self.start_step("上传一个小游戏开发版本，并获取开发版本version_id和小游戏版本号")
        develop_version_id, version_str = OpenApiMngGameFunctionUtils.create_mng_develop_version(self, mng_id, mini_team_id, app_team_id)

        self.start_step("提交小游戏版本审核，并审核通过")
        OpenApiMngGameFunctionUtils.submit_mng_version_audit_and_audit_pass(self, develop_version_id)

        self.start_step("小游戏版本发布上线")
        OpenApiMngGameFunctionUtils.submit_online_mng_version(self, develop_version_id)

        time.sleep(60)

        self.start_step("客户端APP拉到对应版本的小游戏")
        request_dict = AppApiRequestData.check_update_request_data
        request_dict["localMiniAppList"]["value"][0]["value"]["appId"]["value"] = mng_id
        response_dict = AppApiResponseStructure.check_update_response_structure_data
        resp = AppApiUtils.app_api_request(app_team_id, application_id, request_dict, response_dict, 3420, 13420)
        self.assert_equals("检查拉到的小游戏版本", resp["updateList"]["value"][0]["value"]["version"]["value"], version_str)


if __name__ == '__main__':
    CoreProcessTestcase().debug_run()
    jpype.shutdownJVM()
