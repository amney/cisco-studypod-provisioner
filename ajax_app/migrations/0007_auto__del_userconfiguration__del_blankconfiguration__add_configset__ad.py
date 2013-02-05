# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserConfiguration'
        db.delete_table('ajax_app_userconfiguration')

        # Deleting model 'BlankConfiguration'
        db.delete_table('ajax_app_blankconfiguration')

        # Adding model 'ConfigSet'
        db.create_table('ajax_app_configset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blank', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('study_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.StudyType'])),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('create_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modify_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('ajax_app', ['ConfigSet'])

        # Adding model 'Config'
        db.create_table('ajax_app_config', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('configuration', self.gf('django.db.models.fields.TextField')()),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.Device'])),
            ('config_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.ConfigSet'])),
            ('create_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modify_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('ajax_app', ['Config'])


    def backwards(self, orm):
        # Adding model 'UserConfiguration'
        db.create_table('ajax_app_userconfiguration', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('study_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.StudyType'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.Device'])),
            ('configuration', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ajax_app', ['UserConfiguration'])

        # Adding model 'BlankConfiguration'
        db.create_table('ajax_app_blankconfiguration', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('study_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.StudyType'])),
            ('device_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.DeviceType'])),
            ('configuration', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ajax_app', ['BlankConfiguration'])

        # Deleting model 'ConfigSet'
        db.delete_table('ajax_app_configset')

        # Deleting model 'Config'
        db.delete_table('ajax_app_config')


    models = {
        'ajax_app.booking': {
            'Meta': {'unique_together': "(('pod', 'date', 'start_time', 'end_time'),)", 'object_name': 'Booking'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 30, 0, 0)'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Pod']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(0, 0)'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'ajax_app.config': {
            'Meta': {'object_name': 'Config'},
            'config_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.ConfigSet']"}),
            'configuration': ('django.db.models.fields.TextField', [], {}),
            'create_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Device']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ajax_app.configset': {
            'Meta': {'object_name': 'ConfigSet'},
            'blank': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'create_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'study_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.StudyType']"}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'ajax_app.connection': {
            'Meta': {'unique_together': "(('ipv4', 'port'),)", 'object_name': 'Connection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipv4': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'ajax_app.device': {
            'Meta': {'object_name': 'Device'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'devicetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.DeviceType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Location']"}),
            'pod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Pod']", 'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'device_serial'", 'unique': 'True', 'null': 'True', 'to': "orm['ajax_app.Connection']"}),
            'serial_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'ssh': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'device_ssh'", 'unique': 'True', 'null': 'True', 'to': "orm['ajax_app.Connection']"}),
            'telnet': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'device_telnet'", 'unique': 'True', 'null': 'True', 'to': "orm['ajax_app.Connection']"})
        },
        'ajax_app.devicetype': {
            'Meta': {'unique_together': "(('type', 'model', 'ram'),)", 'object_name': 'DeviceType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '25'}),
            'ram': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'RT'", 'max_length': '3'})
        },
        'ajax_app.location': {
            'Meta': {'unique_together': "(('row', 'rack'),)", 'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rack': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'ajax_app.pod': {
            'Meta': {'object_name': 'Pod'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'study_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ajax_app.StudyType']", 'symmetrical': 'False'})
        },
        'ajax_app.studytype': {
            'Meta': {'object_name': 'StudyType'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['ajax_app']