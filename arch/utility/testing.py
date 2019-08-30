from __future__ import absolute_import, division

from collections import OrderedDict

from scipy.stats import chi2

from property_cached import cached_property

__all__ = ['WaldTestStatistic']


class WaldTestStatistic(object):
    """
    Test statistic holder for Wald-type tests

    Parameters
    ----------
    stat : float
        The test statistic
    df : int
        Degree of freedom.
    null : str
        A statement of the test's null hypothesis
    alternative : str
        A statement of the test's alternative hypothesis
    name : str, optional
        Name of test
    """

    def __init__(self, stat, df, null, alternative, name=None):
        self._stat = stat
        self._null = null
        self._alternative = alternative
        self.df = df
        self._name = name
        self.dist = chi2(df)
        self.dist_name = 'chi2({0})'.format(df)

    @property
    def stat(self):
        """Test statistic"""
        return self._stat

    @cached_property
    def pval(self):
        """P-value of test statistic"""
        return 1 - self.dist.cdf(self.stat)

    @cached_property
    def critical_values(self):
        """Critical values test for common test sizes"""
        return OrderedDict(zip(['10%', '5%', '1%'],
                               self.dist.ppf([.9, .95, .99])))

    @property
    def null(self):
        """Null hypothesis"""
        return self._null

    @property
    def alternative(self):
        return self._alternative

    def __str__(self):
        name = '' if not self._name else self._name + '\n'
        msg = '{name}H0: {null}\n{name}H1: {alternative}\nStatistic: {stat:0.4f}\n' \
              'P-value: {pval:0.4f}\nDistributed: {dist}'
        return msg.format(name=name, null=self.null, alternative=self.alternative,
                          stat=self.stat, pval=self.pval, dist=self.dist_name)

    def __repr__(self):
        return self.__str__() + '\n' + \
               self.__class__.__name__ + \
               ', id: {0}'.format(hex(id(self)))