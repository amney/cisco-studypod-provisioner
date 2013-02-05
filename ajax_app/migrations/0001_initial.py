# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DeviceType'
        db.create_table('ajax_app_devicetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ram', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('ajax_app', ['DeviceType'])

        # Adding model 'Connection'
        db.create_table('ajax_app_connection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ipv4', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('port', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('ajax_app', ['Connection'])

        # Adding model 'Pod'
        db.create_table('ajax_app_pod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ajax_app', ['Pod'])

        # Adding model 'Device'
        db.create_table('ajax_app_device', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('telnet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='device_telnet', null=True, to=orm['ajax_app.Connection'])),
            ('ssh', self.gf('django.db.models.fields.related.ForeignKey')(related_name='device_ssh', null=True, to=orm['ajax_app.Connection'])),
            ('serial', self.gf('django.db.models.fields.related.ForeignKey')(related_name='device_serial', null=True, to=orm['ajax_app.Connection'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('devicetype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.DeviceType'], null=True, blank=True)),
            ('pod', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.Pod'], null=True, blank=True)),
        ))
        db.send_create_signal('ajax_app', ['Device'])

        # Adding model 'StudyType'
        db.create_table('ajax_app_studytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('ajax_app', ['StudyType'])

        # Adding model 'Booking'
        db.create_table('ajax_app_booking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pod', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ajax_app.Pod'])),
        ))
        db.send_create_signal('ajax_app', ['Booking'])


    def backwards(self, orm):
        # Deleting model 'DeviceType'
        db.delete_table('ajax_app_devicetype')

        # Deleting model 'Connection'
        db.delete_table('ajax_app_connection')

        # Deleting model 'Pod'
        db.delete_table('ajax_app_pod')

        # Deleting model 'Device'
        db.delete_table('ajax_app_device')

        # Deleting model 'StudyType'
        db.delete_table('ajax_app_studytype')

        # Deleting model 'Booking'
        db.delete_table('ajax_app_booking')


    models = {
        'ajax_app.booking': {
            'Meta': {'object_name': 'Booking'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Pod']"})
        },
        'ajax_app.connection': {
            'Meta': {'object_name': 'Connection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipv4': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'ajax_app.device': {
            'Meta': {'object_name': 'Device'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'devicetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.DeviceType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Pod']", 'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'device_serial'", 'null': 'True', 'to': "orm['ajax_app.Connection']"}),
            'serial_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'ssh': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'device_ssh'", 'null': 'True', 'to': "orm['ajax_app.Connection']"}),
            'telnet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'device_telnet'", 'null': 'True', 'to': "orm['ajax_app.Connection']"})
        },
        'ajax_app.devicetype': {
            'Meta': {'object_name': 'DeviceType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ram': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ajax_app.pod': {
            'Meta': {'object_name': 'Pod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ajax_app.studytype': {
            'Meta': {'object_name': 'StudyType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['ajax_app']