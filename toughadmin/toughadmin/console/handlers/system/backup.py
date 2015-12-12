#!/usr/bin/env python
# coding:utf-8
import os
import os.path
import cyclone.auth
import cyclone.escape
import cyclone.web
from twisted.python import log
from toughadmin.common import utils
from toughadmin.console.handlers.base import BaseHandler, MenuSys
from toughadmin.common.permit import permit
from toughadmin.common.backup import dumpdb,restoredb
from toughadmin.common.config import find_config

@permit.route(r"/backup", u"数据备份管理", MenuSys, order=1.0400, is_menu=True)
class BackupHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        backup_path = self.settings.get('backup_path', '/var/toughadmin/data')
        try:
            if not os.path.exists(backup_path):
                os.makedirs(backup_path)
        except:
            pass
        flist = os.listdir(backup_path)
        flist.sort(reverse=True)
        return self.render("backup_db.html", backups=flist[:30], backup_path=backup_path)

@permit.route(r"/backup/dump", u"备份数据", MenuSys, order=1.0401, is_menu=False)
class DumpHandler(BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        backup_path = self.settings.backup_path
        backup_file = "toughadmin_db_%s.json.gz" % utils.gen_backep_id()
        try:
            dumpdb(find_config(self.settings.cfgfile), os.path.join(backup_path, backup_file))
            return self.render_json(code=0, msg="backup done!")
        except Exception as err:
            log.err()
            return self.render_json(code=1, msg="backup fail! %s" % (err))

@permit.route(r"/backup/restore", u"恢复数据", MenuSys, order=1.0402, is_menu=False)
class RestoreHandler(BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        backup_path = self.settings.backup_path
        backup_file = "toughradius_db_%s.before_restore.json.gz" % utils.gen_backep_id()
        rebakfs = self.get_argument("bakfs")
        try:
            dumpdb(find_config(self.settings.cfgfile), os.path.join(backup_path, backup_file))
            restoredb(find_config(self.settings.cfgfile), os.path.join(backup_path, rebakfs))
            return self.render_json(code=0, msg="restore done!")
        except Exception as err:
            return self.render_json(code=1, msg="restore fail! %s" % (err))


@permit.route(r"/backup/delete", u"删除数据", MenuSys, order=1.0404, is_menu=False)
class DeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        backup_path = self.settings.backup_path
        bakfs = self.get_argument("bakfs")
        try:
            os.remove(os.path.join(backup_path, bakfs))
            return self.render_json(code=0, msg="delete done!")
        except Exception as err:
            return self.render_json(code=1, msg="delete fail! %s" % (err))


@permit.route(r"/backup/upload", u"上传数据", MenuSys, order=1.0403, is_menu=False)
class UploadHandler(BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        try:
            f = self.request.files['Filedata'][0]
            save_path = os.path.join(self.settings.backup_path, f['filename'])
            tf = open(save_path, 'wb')
            tf.write(f['body'])
            tf.close()
            self.write("upload success")
        except Exception as err:
            self.write("upload fail %s" % str(err))









