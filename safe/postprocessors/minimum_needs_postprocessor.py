# -*- coding: utf-8 -*-
"""**Postprocessors package.**

"""

__author__ = 'Marco Bernasocchi <marco@opengis.ch>'
__revision__ = '$Format:%H$'
__date__ = '22/08/2013'
__license__ = "GPL"
__copyright__ = 'Copyright 2012, Australia Indonesia Facility for '
__copyright__ += 'Disaster Reduction'


from safe.postprocessors.abstract_postprocessor import AbstractPostprocessor

from safe.common.utilities import (ugettext as tr)
from safe.impact_functions.core import evacuated_population_weekly_needs


class MinimumNeedsPostprocessor(AbstractPostprocessor):
    """
    Postprocessor that aggregates minimum needs.
    see the _calculate_* methods to see indicator specific documentation

    see :mod:`safe.defaults` for default values information
    """

    def __init__(self):
        """
        Constructor for MinimumNeedsPostprocessor postprocessor class,
        It takes care of defining self.impact_total
        """
        AbstractPostprocessor.__init__(self)
        self.impact_total = None

    def description(self):
        """Describe briefly what the post processor does.

        Args:
            None

        Returns:
            Str the translated description

        Raises:
            Errors are propagated
        """
        return tr('Aggregates minimum needs.')

    def setup(self, params):
        """concrete implementation it takes care of the needed parameters being
         initialized

        Args:
            params: dict of parameters to pass to the post processor
        Returns:
            None
        Raises:
            None
        """
        AbstractPostprocessor.setup(self, None)
        if self.impact_total is not None:
            self._raise_error('clear needs to be called before setup')

        self.impact_total = int(round(params['impact_total']))
        # print params

    def process(self):
        """concrete implementation it takes care of the needed parameters being
         available and performs all the indicators calculations

        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        AbstractPostprocessor.process(self)
        if self.impact_total is None:
            self._log_message('%s not all params have been correctly '
                              'initialized, setup needs to be called before '
                              'process. Skipping this postprocessor'
                              % self.__class__.__name__)
        else:
            self._calculate_needs()

    def clear(self):
        """concrete implementation it takes care of the needed parameters being
         properly cleared

        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        AbstractPostprocessor.clear(self)
        self.impact_total = None

    def _calculate_needs(self):
        """Indicator that shows aggregated minimum needs.

        this indicator reports the aggregated minimum needs

        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        myNeeds = evacuated_population_weekly_needs(self.impact_total,
                                                    human_names=True)

        for need, value in myNeeds.iteritems():
            try:
                myResult = int(round(value))
            except ValueError:
                myResult = self.NO_DATA_TEXT

            self._append_result(need, myResult)
