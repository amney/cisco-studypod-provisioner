# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Booking.start_datetime'
        db.alter_column('ajax_app_booking', 'start_datetime', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Booking.end_datetime'
        db.alter_column('ajax_app_booking', 'end_datetime', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # Changing field 'Booking.start_datetime'
        db.alter_column('ajax_app_booking', 'start_datetime', self.gf('django.db.models.fields.TimeField')())

        # Changing field 'Booking.end_datetime'
        db.alter_column('ajax_app_booking', 'end_datetime', self.gf('django.db.models.fields.TimeField')())

    models = {
        'ajax_app.booking': {
            'Meta': {'unique_together': "(('pod', 'start_datetime', 'end_datetime'),)", 'object_name': 'Booking'},
            'config_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.ConfigSet']"}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Pod']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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