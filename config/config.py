# -*- coding: UTF-8 -*-


import sys


reload(sys)
sys.setdefaultencoding("utf-8")

ip_address = '127.0.0.1'
port = 27017
thread_num = 8

items = {
    'basic_info': {
        'td_items': [
            (u'统一社会信用代码|组织机构代码', 'code'),
            (u'公益性捐赠税前扣除资格', 'qualification'),  # 旧版本没有
            (u'非营利组织免税资格', 'tax_qualification'),  # 旧版本没有
            (u'业务主管单位', 'business_unit'),
            (u'成立时间', 'established_time'),  # 格式未统一
            (u'秘书长', 'secretary_general'),  # 旧版本不一样
            (u'理事长', 'president'),
            (u'理事数', 'director_number'),
            (u'监事数', 'supervisor_number'),
            (u'负责人中担任过省部级及以上领导职务的人数', 'province_number'),
            (u'负责人中现任国家工作人员的人数|负责人中现任国家工作人员数', 'country_number'),
            (u'负责人数', 'responsible_number'),
            (u'专项基金数', 'special_found'),
            (u'代表机构数', 'representative_institution_number'),
            (u'持有股权的实体数', 'physical_stock_number'),
            (u'专职工作人员数', 'staff_number'),
            (u'志愿者数', 'volunteer_number'),
            (u'举办刊物情况', 'publication'),
            (u'会计师事务所名称', 'accounting_firm'),  # 旧版本没有
            (u'审计意见类型', 'audit opinion'),  # 旧版本没有
        ],
        'check_items': [
            (u'项目管理制度', 'project_management', u"项目管理制度</td>.+?checkbox_black\.gif\' width=\'10\' height=\'10\'>&nbsp;(\D)"),
            (u'财务管理制度', 'financial_management', u"财务管理制度</td>.+?checkbox_black\.gif\' width=\'10\' height=\'10\'>&nbsp;(\D)"),
            (u'基金会类型', 'foundation_type'),
        ],
        'match_items': [
            (u'理事会召开次数', 'council_number', u'本年度共召开\((\d+)\)次理事会'),
        ],
        'input_items': [
            (u'项目数量', 'project_number', 'huodongshu', "huodongshu\'  value=\'(\d+)\'  CLASS"),  # 旧版本识别不出来。。
        ]

    },

    'assets_info': {
        'td_items': [
            (u'货币资金', 'currency'),
            (u'短期借款', 'short_loan'),
            (u'短期投资', 'short_investment'),
            (u'应付款项', 'pay'),
            (u'应收款项', 'receive'),
            (u'应付工资', 'salary'),
            (u'预付账款', 'prepay'),
            (u'应交税金', 'deal'),
            (u'存 货', 'stock'),
            (u'预收账款', 'pre_receive'),
            (u'待摊费用', 'expense'),
            (u'预提费用', 'pre_expense'),
            (u'一年内到期的长期债权投资', 'year_investment'),
            (u'预计负债', 'estimated_liabilities'),
            (u'其他流动资产', 'liquid_assets'),
            (u'一年内到期的长期负债', 'year_liabilities'),
            (u'流动资产合计', 'total_liquid_assets'),
            (u'其他流动负债', 'liquid_liabilities'),
            (u'流动负债合计', 'total_liquid_liabilities'),
            (u'长期股权投资', 'long_investment'),
            (u'长期债权投资', 'long_claim_investment'),
            (u'长期借款', 'long_loan'),
            (u'长期投资合计', 'total_long_investment'),
            (u'长期应付款', 'long_pay'),
            (u'其他长期负债', 'long_liabilities'),
            (u'固定资产原价', 'fixed_assets'),
            (u'长期负债合计', 'total_long_liabilities'),
            (u'累计折旧', 'depreciation'),
            (u'固定资产净值', 'fixed_assets_value'),
            (u'受托代理负债', 'proxy_liabilities'),
            (u'在建工程', 'project_on_building'),
            (u'负债合计', 'total_liabilities'),
            (u'文物文化资产', 'culture_assets'),
            (u'固定资产清理', 'fixed_assets_clean'),
            (u'非限定性净资产', 'non_limiting_assets'),
            (u'固定资产合计', 'total_fixed_assets'),
            (u'限定性净资产', 'limiting_assets'),
            (u'净资产合计', 'total_assets_value'),
            (u'无形资产', 'intangible_assets'),
            (u'负债和净资产合计', 'total_liabilities_assets'),
            (u'受托代理资产', 'proxy_assets'),
            (u'资产总计', 'total_assets')
        ]
    },

    'cash_info': {
        'td_items': [
            (u'接受捐赠收到的现金', 'donate_cash'),
            (u'收取会费收到的现金', 'fees_cash'),
            (u'提供服务收到的现金', 'service_cash'),
            (u'销售商品收到的现金', 'sales_cash'),
            (u'政府补助收到的现金', 'gov_cash'),
            (u'收到的其他与业务活动有关的现金', 'other_business_cash'),
            (u'现金流入小计', 'total_business_income', 0),
            (u'提供捐赠或者资助支付的现金', 'donate_pay'),
            (u'支付给员工以及为员工支付的现金', 'staff_pay'),
            (u'购买商品、接受服务支付的现金', 'sales_pay'),
            (u'支付的其他与业务活动有关的现金', 'other_business_pay'),
            (u'现金流出小计', 'total_business_out', 0),
            (u'业务活动产生的现金流量净额', 'business_value'),


            (u'收回投资所收到的现金', 'investment_recover_cash'),
            (u'取得投资收益所收到的现金', 'investment_receive_cash'),
            (u'处置固定资产和无形资产所收回的现金', 'assets_cash'),
            (u'收到的其他与投资活动有关的现金', 'other_investment_cash'),
            (u'现金流入小计', 'total_investment_income', 1),
            (u'购建固定资产和无形资产所支付的现金', 'assets_pay'),
            (u'对外投资所支付的现金', 'investment_pay'),
            (u'支付的其他与投资活动有关的现金', 'other_investment_pay'),
            (u'现金流出小计', 'total_investment_out', 1),
            (u'投资活动产生的现金流量净额', 'investment_value'),

            (u'借款所收到的现金', 'loan_cash'),
            (u'收到的其他与筹资活动有关的现金', 'other_financing_cash'),
            (u'现金流入小计', 'total_financing_income', 2),
            (u'偿还借款所支付的现金|偿还债款所支付的现金', 'loan_pay'),
            (u'偿付利息所支付的现金', 'interest_cash'),
            (u'支付的其他与筹资活动有关的现金', 'other_financing_pay'),
            (u'现金流出小计', 'total_financing_out', 2),
            (u'筹资活动产生的现金流量净额|投资活动产生的现金流量净额', 'financing_value'),

            (u'四、汇率变动对现金的影响额', 'exchange_rate_value'),

            (u'五、现金及现金等价物净增加额', 'cash_value')
        ]
    },

    'welfare_info': {
        'td_items': [
            (u'本年捐赠收入（自动求和）|本年捐赠收入', 'year_donate', 1),
            (u'来自境内的捐赠（自动求和）|来自境内的捐赠', 'domestic_donation', 1),
            (u'来自境内自然人的捐赠', 'domestic_natural_donation', 1),
            (u'来自境内法人或.{0,1}其他组织的捐赠', 'domestic_legal_donation', 1),
            (u'来自其他基金会的捐赠', 'other_foudatin_donation', 1),
            (u'来自境外的捐赠（自动求和）|来自境外的捐赠', 'overseas_donation', 1),
            (u'来自境外自然人的捐赠', 'overseas_natural_donation', 1),
            (u'来自境外法人或.{0,1}其他组织的捐赠', 'overseas_legal_donation', 1),

            # (u'（对捐赠人构成利益回报条件的赠与或不符合公益性目的赠与）', 'non_profit_donate', 1), # 2017没有这个
            (u'二、大额捐赠收入情况', 'big_donate', 2),  #2017 为 二、

        #     (u'上年度基金余额|上年末净资产', 'last_year_value', 3),
        #     (u'上年度实际收入合计', 'last_actual_income', 3),
        #     (u'调整后的上年度总收入', 'last_adjust_income', 3),
        #     (u'本年度总支出', 'year_pay', 3),
        #     (u'年度用于慈善活动的支出|本年度用于公益事业的支出', 'year_charity_pay', 3),
        #     (u'工作人员工资福利支出', 'wage_pay', 3),
        #     (u'行政办公支出', 'admin_pay', 3),
        #     # (u'管理费用', 'manage_pay', 3),
        #     (u'其他支出', 'other_pay', 3),
        #     (u'本年度公益事业支出占上年度基金余额的比例（综合近两年比例，综合近三年比例）|本年度慈善活动支出占上年末净资产的比例（占前三年年末净资产平均数的比例）', 'charity_scale', 3),
        #     (u'工作人员工资福利和行政办公支出占总支出的比例（综合近两年比例，综合近三年比例）|本年度管理费用占总支出的比例', 'manage_scale', 3),
        ]
    },

    'public_info': {
        'check_items': [
            (u'公开经民政部门核准的章程', 'regulation_public'),
            (u'公开理事长、副理事长、秘书长、理事、监事的基本情况', 'basic_public'),
            (u'公开下设的秘书处组成部门、专项基金和其他机构的名称、设立时间、存续情况、业务范围或者主要职能', 'secretariat_public'),
            (u'公开重要关联方', 'relate_public'),
            (u'公开联系人、联系方式.门户网站、官方微博、官方微信或者移动客户端等网络平台', 'contact_public'),
            (u'公开信息公开制度、项目管理制度、财务和资产管理制度', 'system_public'),
            (u'公开领取薪酬最高前五位人员的职务和薪酬', 'five_public'),
            (u'公开因公出国（境）经费、公务用车购置及运行费用、公务招待费用、公务差旅费用标准', 'travel_public'),
            (u'公开募捐方案', 'donate_public'),
            (u'公开募捐取得的款物等收入情况', 'receive_public'),
            (u'公开已经使用的募得款物的用途', 'use_public'),
            (u'公开尚未使用的募捐款物的使用计划', 'unused_public'),
            (u'公开公益慈善项目内容、实施地域、受益人群', 'donate_item_public'),
            (u'公开公益慈善项目收入、支出情况', 'detail_public'),
            (u'公开公益慈善项目剩余财产处理情况', 'remaining_public'),
            (u'公开慈善信托信息', 'trust_public'),
            (u'公开重大资产变动情况、重大投资活动情况', 'big_investment_public'),
            (u'公开重大交易或者资金往来情况', 'big_deal_public'),
            (u'公开关联交易情况', 'relate_transaction_public'),
        ]
    },

    'business_info': {
        'td_items': [

            (u'其他费用|其 他 费 用|其  他  费  用', 'other_cost'),
            (u'会费收入', 'fees_income'),
            (u'收入合计|收 入 合 计|收  入  合  计', 'total_income'),
            (u'筹资费用|筹 资 费 用|筹  资  费  用', 'funding_cost'),
            (u'业务活动成本|业 务 活 动 成 本', 'business_cost'),
            (u'提供服务收入', 'service_income'),
            (u'投资收益', 'investment_income'),
            (u'政府补助收入', 'gov_income'),
            (u'管理费用|管 理 费 用|管  理  费  用', 'manage_cost'),
            (u'商品销售收入', 'sales_income'),
            (u'捐赠收入|其中：捐赠收入', 'donate_income'),
            (u'其他收入', 'other_income'),
            (u'限定性净资产转为非限定性净资产', 'year_investment'),
            (u'净资产变动额（若为净资产减少额，以“-”号填列）|净资产变动额（若为净资产减少额，以“－"号填列）|净资产变动额（若为净资产减少额，以“－”号填列）', 'estimated_liabilities'),
            (u'费用合计|费 用 合 计', 'total_cost'),

        ]
    }
}



