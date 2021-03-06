#!/usr/bin/env python
#coding:utf-8
import warnings

import sqlalchemy

warnings.simplefilter('ignore', sqlalchemy.exc.SAWarning)
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


def get_metadata(db_engine):
    global DeclarativeBase
    metadata = DeclarativeBase.metadata
    metadata.bind = db_engine
    return metadata


class SystemSession(DeclarativeBase):
    """session表"""
    __tablename__ = 'system_session'

    __table_args__ = {
        'mysql_engine' : 'MEMORY'
    }

    key = Column(u'_key', Unicode(length=512), primary_key=True, nullable=False,doc=u"session key")
    value = Column(u'_value', Unicode(length=2048), nullable=False,doc=u"session value")
    time = Column(u'_time', INTEGER(), nullable=False,doc=u"session timeout")

class SystemCache(DeclarativeBase):
    """cache表"""
    __tablename__ = 'system_cache'

    __table_args__ = {
        'mysql_engine' : 'MEMORY'
    }

    key = Column(u'_key', Unicode(length=512), primary_key=True, nullable=False,doc=u"cache key")
    value = Column(u'_value', Unicode(length=4096), nullable=False,doc=u"cache value")
    time = Column(u'_time', INTEGER(), nullable=False,doc=u"cache timeout")



class TrwOperator(DeclarativeBase):
    """操作员表 操作员类型 0 系统管理员 1 普通操作员"""
    __tablename__ = 'trw_operator'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"操作员id")
    operator_type = Column('operator_type', INTEGER(), nullable=False,doc=u"操作员类型")
    operator_name = Column(u'operator_name', Unicode(32), nullable=False,doc=u"操作员名称")
    operator_pass = Column(u'operator_pass', Unicode(length=128), nullable=False,doc=u"操作员密码")
    operator_status = Column(u'operator_status', INTEGER(), nullable=False,doc=u"操作员状态,0/1")
    operator_desc = Column(u'operator_desc', Unicode(255), nullable=False,doc=u"操作员描述")

class TrwOperatorRule(DeclarativeBase):
    """操作员权限表"""
    __tablename__ = 'trw_operator_rule'

    __table_args__ = {}
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"权限id")
    operator_name = Column(u'operator_name', Unicode(32), nullable=False,doc=u"操作员名称")
    rule_path = Column(u'rule_path', Unicode(128), nullable=False,doc=u"权限URL")
    rule_name = Column(u'rule_name', Unicode(128), nullable=False,doc=u"权限名称")
    rule_category = Column(u'rule_category', Unicode(128), nullable=False,doc=u"权限分类")


class TrwParam(DeclarativeBase):
    """系统参数表  """
    __tablename__ = 'trw_param'

    __table_args__ = {}

    #column definitions
    param_name = Column(u'param_name', Unicode(length=64), primary_key=True, nullable=False,doc=u"参数名")
    param_value = Column(u'param_value', Unicode(length=1024), nullable=False,doc=u"参数值")
    param_desc = Column(u'param_desc', Unicode(length=255),doc=u"参数描述")

class TrwIsp(DeclarativeBase):
    """运营商,状态 0-正常，1-暂停服务
    """
    __tablename__ = 'trw_isp'

    __table_args__ = {}

    isp_code = Column('isp_code', Unicode(length=16), primary_key=True,nullable=False)
    isp_name = Column('isp_name', Unicode(length=128), nullable=False)
    isp_desc = Column('isp_desc', Unicode(length=255))   
    isp_email = Column('isp_email',Unicode(length=128))
    isp_phone = Column('isp_phone',Unicode(length=64))
    isp_idcard = Column('isp_idcard',Unicode(length=64))
    user_total = Column(u'user_total', INTEGER(), nullable=False, doc=u"用户数")
    status = Column('status', SMALLINT(), nullable=False)

class TrwIspService(DeclarativeBase):
    """运营商服务
    """
    __tablename__ = 'trw_isp_service'

    __table_args__ = {}

    isp_code = Column('isp_code', Unicode(length=16), primary_key=True,nullable=False)
    service_type = Column('service_type', Unicode(length=16), primary_key=True, nullable=False)
    bill_times = Column(u'bill_times', INTEGER(), nullable=False,default=0, doc=u"已经计费时长-秒")
    sub_time = Column(u'sub_time', Unicode(length=19), nullable=False, doc=u"订阅时间")


class TrwBas(DeclarativeBase):
    """BAS设备表 """
    __tablename__ = 'trw_bas'

    __table_args__ = {}

    # column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"设备id")
    isp_code = Column('isp_code', Unicode(length=8),nullable=False)
    ip_addr = Column(u'ip_addr', Unicode(length=15), index=True, nullable=True, doc=u"IP地址")
    dns_name = Column(u'dns_name', Unicode(length=128), nullable=True, doc=u"DNS名称")
    bas_name = Column(u'bas_name', Unicode(length=64), nullable=False, doc=u"bas名称")
    bas_secret = Column(u'bas_secret', Unicode(length=64), nullable=False, doc=u"共享密钥")
    vendor_id = Column(u'vendor_id', INTEGER(), nullable=False, doc=u"bas类型")
    portal_vendor = Column(u'portal_vendor', Unicode(length=64), nullable=False, doc=u"portal协议")
    time_type = Column(u'time_type', SMALLINT(), nullable=False, doc=u"时区类型")
    ac_port = Column(u'ac_port', INTEGER(), nullable=False, doc=u"AC端口")
    coa_port = Column(u'coa_port', INTEGER(), nullable=False, doc=u"CoA端口")

    # relation definiti



class TrwDomain(DeclarativeBase):
    """域属性表 """
    __tablename__ = 'trw_domain'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"id")
    isp_code = Column('isp_code', Unicode(length=8),nullable=False)
    domain_code = Column(u'domain_code', Unicode(length=16), nullable=False, index=True, doc=u"域编码")
    tpl_name = Column(u'tpl_name', Unicode(length=64), nullable=False, doc=u"模版名称")
    domain_desc = Column(u'domain_desc', Unicode(length=64), nullable=False, doc=u"域描述")
    UniqueConstraint('isp_code', 'domain_code', name='unique_isp_domain')

class TrwDomainAttr(DeclarativeBase):
    """portal模版属性 """
    __tablename__ = 'trw_domain_attr'

    __table_args__ = {}

    # column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"模版属性id")
    isp_code = Column('isp_code', Unicode(length=8), nullable=False)
    domain_code = Column(u'domain_code', Unicode(length=16), nullable=False, doc=u"域编码")
    attr_name = Column(u'attr_name', Unicode(length=128), nullable=False, doc=u"模版名")
    attr_value = Column(u'attr_value', Unicode(length=1024), nullable=False, doc=u"属性值")
    attr_desc = Column(u'attr__desc', Unicode(length=255), doc=u"属性描述")
    UniqueConstraint('isp_code', 'domain_code',"attr_name", name='unique_isp_domain_attr')

class TrwSsid(DeclarativeBase):
    """SSID信息表 """
    __tablename__ = 'trw_ssid'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"id")
    isp_code = Column('isp_code', Unicode(length=8), nullable=False)
    domain_code = Column(u'domain_code', Unicode(length=16), nullable=False,doc=u"域编码")
    ssid = Column(u'ssid', Unicode(length=16), nullable=False, index=True, doc=u"ssid")
    ssid_desc = Column(u'ssid_desc', Unicode(length=64), nullable=False, doc=u"ssid描述")
    UniqueConstraint('isp_code', 'domain_code',"ssid", name='unique_isp_domain_ssid')


class TrwRadius(DeclarativeBase):
    """radius节点表 """
    __tablename__ = 'trw_radius'

    __table_args__ = {}

    # column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"设备id")
    ip_addr = Column(u'ip_addr', Unicode(length=15), nullable=False, doc=u"IP地址")
    serv_type = Column(u'serv_type', INTEGER(),doc=u"Radius服务器类型，master/slave")
    name = Column(u'name', Unicode(length=64), nullable=False, doc=u"radius名称")
    secret = Column(u'secret', Unicode(length=64), nullable=False, doc=u"共享密钥")
    auth_port = Column(u'auth_port', INTEGER(), nullable=False, doc=u"认证端口")
    acct_port = Column(u'acct_port', INTEGER(), nullable=False, doc=u"记账端口")
    api_secret = Column(u'api_secret', Unicode(length=255), nullable=False, doc=u"API密钥")
    api_url = Column(u'api_url', Unicode(length=255), nullable=False, doc=u"API地址")
    last_check = Column(u'last_check', Unicode(length=19), nullable=True, doc=u"最后检测")


class TrwTemplate(DeclarativeBase):
    """portal模版 """
    __tablename__ = 'trw_template'

    __table_args__ = {}

    # column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"模版id")
    tpl_name = Column(u'tpl_name', Unicode(length=64), nullable=False, doc=u"模版名称")
    tpl_desc = Column(u'tpl_desc', Unicode(length=512), nullable=False, doc=u"模版描述")
    UniqueConstraint('isp_code', 'tpl_name', name='unique_isp_tempalte')



class TrwOperateLog(DeclarativeBase):
    """操作日志表"""
    __tablename__ = 'trw_operate_log'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"日志id")
    operator_name = Column(u'operator_name', Unicode(32), nullable=False,doc=u"操作员名称")
    operate_ip = Column(u'operate_ip', Unicode(length=128),doc=u"操作员ip")
    operate_time = Column(u'operate_time', Unicode(length=19), nullable=False,doc=u"操作时间")
    operate_desc = Column(u'operate_desc', Unicode(length=1024),doc=u"操作描述")


class TrwOSTypes(DeclarativeBase):
    """设备类型"""
    __tablename__ = 'trw_os_types'

    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"编号")
    os_name = Column(u'os_name', Unicode(length=32), nullable=False, doc=u"操作系统类型")
    dev_type = Column(u'dev_type', Unicode(length=32), nullable=False, doc=u"设备类型")
    match_rule = Column(u'match_rule', Unicode(length=255), nullable=False, doc=u"匹配规则")




