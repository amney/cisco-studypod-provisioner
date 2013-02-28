# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DeviceType'
        db.create_table('ajax_app_devicetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='RT', max_length=3)),
            ('model', self.gf('django.db.models.fields.CharField')(default=0, max_length=25)),
            ('ram', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('ajax_app', ['DeviceType'])

        # Adding unique constraint on 'DeviceType', fields ['type', 'model', 'ram']
        db.create_unique('ajax_app_devicetype', ['type', 'model', 'ram'])

        # Adding model 'Connection'
        db.create_table('ajax_app_connection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ipv4', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('port', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('ajax_app', ['Connection'])

        # Adding unique constraint on 'Connection', fields ['ipv4', 'port']
        db.create_unique('ajax_app_connection', ['ipv4', 'port'])

        # Adding model 'Location'
        db.create_table('ajax_app_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('row', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('rack', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
        ))
        db.send_create_signal('ajax_app', ['Location'])

        # Adding unique constraint on 'Location', fields ['row', 'rack']
        db.create_unique('ajax_app_location', ['row', 'rack'])

        # Adding model 'StudyType'
        db.create_table('ajax_app_studytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('ajax_app', ['StudyType'])

        # Adding model 'Pod'
        db.create_table('ajax_app_pod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
        ))
        db.send_create_signal('ajax_app', ['Pod'])

        # Adding M2M table for field study_types on 'Pod'
        db.create_table('ajax_app_pod_study_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pod', models.ForeignKey(orm['ajax_app.pod'], null=False)),
            ('studytype', models.ForeignKey(orm['ajax_app.studytype'], null=False))
        ))
        db.create_unique('ajax_app_pod_study_types', ['pod_id', 'studytype_id'])

        # Adding model 'Device'
        db.create_table('ajax_app_device', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('telnet', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='device_telnet', unique=True, null=True, to=orm['ajax_app.Connection'])),
            ('ssh', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='device_ssh', unique=True, null=True, to=orm['ajax_app.Connection'])),
            ('serial', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='device_serial', unique=True, null=True, to=orm['ajax_app.Connection'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.Location'])),
            ('devicetype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.DeviceType'], null=True, blank=True)),
            ('pod', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.Pod'], null=True, blank=True)),
        ))
        db.send_create_signal('ajax_app', ['Device'])

        # Adding model 'ConfigSet'
        db.create_table('ajax_app_configset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blank', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('study_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.StudyType'])),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('pod', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.Pod'])),
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

        # Adding model 'Booking'
        db.create_table('ajax_app_booking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pod', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.Pod'])),
            ('start_datetime', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime.now)),
            ('end_datetime', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime.now)),
            ('config_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.ConfigSet'])),
        ))
        db.send_create_signal('ajax_app', ['Booking'])

        # Adding unique constraint on 'Booking', fields ['pod', 'start_datetime', 'end_datetime']
        db.create_unique('ajax_app_booking', ['pod_id', 'start_datetime', 'end_datetime'])


    def backwards(self, orm):
        # Removing unique constraint on 'Booking', fields ['pod', 'start_datetime', 'end_datetime']
        db.delete_unique('ajax_app_booking', ['pod_id', 'start_datetime', 'end_datetime'])

        # Removing unique constraint on 'Location', fields ['row', 'rack']
        db.delete_unique('ajax_app_location', ['row', 'rack'])

        # Removing unique constraint on 'Connection', fields ['ipv4', 'port']
        db.delete_unique('ajax_app_connection', ['ipv4', 'port'])

        # Removing unique constraint on 'DeviceType', fields ['type', 'model', 'ram']
        db.delete_unique('ajax_app_devicetype', ['type', 'model', 'ram'])

        # Deleting model 'DeviceType'
        db.delete_table('ajax_app_devicetype')

        # Deleting model 'Connection'
        db.delete_table('ajax_app_connection')

        # Deleting model 'Location'
        db.delete_table('ajax_app_location')

        # Deleting model 'StudyType'
        db.delete_table('ajax_app_studytype')

        # Deleting model 'Pod'
        db.delete_table('ajax_app_pod')

        # Removing M2M table for field study_types on 'Pod'
        db.delete_table('ajax_app_pod_study_types')

        # Deleting model 'Device'
        db.delete_table('ajax_app_device')

        # Deleting model 'ConfigSet'
        db.delete_table('ajax_app_configset')

        # Deleting model 'Config'
        db.delete_table('ajax_app_config')

        # Deleting model 'Booking'
        db.delete_table('ajax_app_booking')


    models = {
        'ajax_app.booking': {
            'Meta': {'unique_together': "(('pod', 'start_datetime', 'end_datetime'),)", 'object_name': 'Booking'},
            'config_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.ConfigSet']"}),
            'end_datetime': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Pod']"}),
            'start_datetime': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime.now'}),
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
            'pod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Pod']"}),
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