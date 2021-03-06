#
# This file is part of the THOR Dashboard Project.
# Copyright (C) 2016 CERN.
#
# The THOR dashboard is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# HEPData is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the THOR dashboard; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

from django.db import models

class Tutor(models.Model):
    verbose_name_plural = "Tutors"
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class EventType(models.Model):
    verbose_name_plural = "Event Types"
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Country(models.Model):
    verbose_name_plural = "Countries"

    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class ParticipantType(models.Model):
    verbose_name_plural = "Participant Types"

    type_choices = (
        ('S', 'Senior Academics'),
        ('PD', 'Post Docs'),
        ('G', 'Grad Students'),
        ('UG', 'Undergrads'),
        ('P', 'Public'),
        ('U', 'Unknown'),
    )
    type = models.CharField(max_length=32, choices=type_choices)

    def __str__(self):
        type = ''
        for item in self.type_choices:
            if item[0] == self.type:
                type = item[1]
        return "{0}".format(type)


class Event(models.Model):
    verbose_name_plural = "Events"

    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    type = models.ForeignKey(EventType, blank=False)

    country = models.ForeignKey(Country, null=True, blank=True)
    participant_type = models.ManyToManyField(ParticipantType)
    participant_count = models.IntegerField(default=0)

    event_url = models.URLField(blank=True, null=True)

    tutors = models.ManyToManyField(Tutor)

    def __str__(self):
        return "{0}-{1} {2} ({3})".format(self.start_date, self.end_date, self.name, self.country)

    def to_dict(self):
        _dict = {'id': self.id, 'name': self.name, 'description': self.description, 'date': self.start_date.__str__(),
                 'type': self.type.name, 'country': self.country.name, 'participant_count': self.participant_count,
                 'event_url': self.event_url, 'tutors':[], 'participant_type': []}

        for participant in self.participant_type.all():
            _dict['participant_type'].append(participant.__str__())

        for tutor in self.tutors.all():
            _dict['tutors'].append(tutor.name)

        return _dict
