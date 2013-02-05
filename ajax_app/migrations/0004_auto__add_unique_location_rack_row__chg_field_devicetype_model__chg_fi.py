# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Location', fields ['rack', 'row']
        db.create_unique('ajax_app_location', ['rack', 'row'])

        # Adding M2M table for field study_types on 'Pod'
        db.create_table('ajax_app_pod_study_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pod', models.ForeignKey(orm['ajax_app.pod'], null=False)),
            ('studytype', models.ForeignKey(orm['ajax_app.studytype'], null=False))
        ))
        db.create_unique('ajax_app_pod_study_types', ['pod_id', 'studytype_id'])


        # Changing field 'DeviceType.model'
        db.alter_column('ajax_app_devicetype', 'model', self.gf('django.db.models.fields.CharField')(max_length=25))

        # Changing field 'DeviceType.type'
        db.alter_column('ajax_app_devicetype', 'type', self.gf('django.db.models.fields.CharField')(max_length=3))
        # Adding unique constraint on 'DeviceType', fields ['model', 'ram', 'type']
        db.create_unique('ajax_app_devicetype', ['model', 'ram', 'type'])

        # Adding unique constraint on 'Connection', fields ['ipv4', 'port']
        db.create_unique('ajax_app_connection', ['ipv4', 'port'])

        # Deleting field 'StudyType.type'
        db.delete_column('ajax_app_studytype', 'type')

        # Adding field 'StudyType.name'
        db.add_column('ajax_app_studytype', 'name',
                      self.gf('django.db.models.fields.CharField')(default='CCNP', max_length=25),
                      keep_default=False)

        # Adding field 'StudyType.description'
        db.add_column('ajax_app_studytype', 'description',
                      self.gf('django.db.models.fields.TextField')(default='A mid-level Cisco qualifaction'),
                      keep_default=False)

        # Adding unique constraint on 'Device', fields ['telnet']
        db.create_unique('ajax_app_device', ['telnet_id'])

        # Adding unique constraint on 'Device', fields ['ssh']
        db.create_unique('ajax_app_device', ['ssh_id'])

        # Adding unique constraint on 'Device', fields ['serial']
        db.create_unique('ajax_app_device', ['serial_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Device', fields ['serial']
        db.delete_unique('ajax_app_device', ['serial_id'])

        # Removing unique constraint on 'Device', fields ['ssh']
        db.delete_unique('ajax_app_device', ['ssh_id'])

        # Removing unique constraint on 'Device', fields ['telnet']
        db.delete_unique('ajax_app_device', ['telnet_id'])

        # Removing unique constraint on 'Connection', fields ['ipv4', 'port']
        db.delete_unique('ajax_app_connection', ['ipv4', 'port'])

        # Removing unique constraint on 'DeviceType', fields ['model', 'ram', 'type']
        db.delete_unique('ajax_app_devicetype', ['model', 'ram', 'type'])

        # Removing unique constraint on 'Location', fields ['rack', 'row']
        db.delete_unique('ajax_app_location', ['rack', 'row'])

        # Removing M2M table for field study_types on 'Pod'
        db.delete_table('ajax_app_pod_study_types')


        # Changing field 'DeviceType.model'
        db.alter_column('ajax_app_devicetype', 'model', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'DeviceType.type'
        db.alter_column('ajax_app_devicetype', 'type', self.gf('django.db.models.fields.IntegerField')(null=True))
        # Adding field 'StudyType.type'
        db.add_column('ajax_app_studytype', 'type',
                      self.gf('django.db.models.fields.TextField')(default='CCNP'),
                      keep_default=False)

        # Deleting field 'StudyType.name'
        db.delete_column('ajax_app_studytype', 'name')

        # Deleting field 'StudyType.description'
        db.delete_column('ajax_app_studytype', 'description')


    models = {
        'ajax_app.booking': {
            'Meta': {'object_name': 'Booking'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Pod']"})
        },
        'ajax_app.connection': {
            'Meta': {'unique_together': "(('ipv4', 'port'),)", 'object_name': 'Connection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipv4': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'ajax_app.device': {
            'Meta': {'object_name': 'Device'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'devicetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.DeviceType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Location']"}),
            'pod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ajax_app.Pod']", 'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'device_serial'", 'unique': 'True', 'null': 'True', 'to': "orm['ajax_app.Connection']"}),
            'serial_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'ssh': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'device_ssh'", 'unique': 'True', 'null': 'True', 'to': "orm['ajax_app.Connection']"}),
            'telnet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'device_telnet'", 'unique': 'True', 'null': 'True', 'to': "orm['ajax_app.Connection']"})
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