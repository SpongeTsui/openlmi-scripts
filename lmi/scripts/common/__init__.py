# Copyright (C) 2013-2014 Red Hat, Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of the FreeBSD Project.
#
# Authors: Michal Minar <miminar@redhat.com>
#
"""
Package with client-side python modules and command line utilities.
"""

import logging

from lmi.shell import LMINamespace
from lmi.shell import LMIExceptions
from lmi.scripts.common.configuration import Configuration
from lmi.scripts.common.lmi_logging import get_logger

LOG = get_logger(__name__)

def get_computer_system(ns):
    """
    Obtain an instance of ``CIM_ComputerSystem`` or its subclass. Preferred
    class name can be configured in configuration file. If such class does
    not exist, a base class (``CIM_ComputerSystem``) is enumerated instead.
    First feasible instance is cached and returned.

    :param ns: Namespace object where to look for computer system class.
    :type ns: :py:class:`lmi.shell.LMINamespace`
    :returns: Instance of ``CIM_ComputerSystem``.
    :rtype: :py:class:`lmi.shell.LMIInstance`.
    """
    if not isinstance(ns, LMINamespace):
        raise TypeError("ns must be an instance of LMINamespace")
    if not hasattr(get_computer_system, '_cs_cache'):
        get_computer_system._cs_cache = {}
    ns_path = ns.connection.uri + '/' + ns.name
    if not ns_path in get_computer_system._cs_cache:
        config = Configuration.get_instance()
        try:
            get_computer_system._cs_cache[ns_path] = cs = \
                    getattr(ns, config.system_class_name).first_instance()
        except LMIExceptions.LMIClassNotFound:
            LOG().warn('failed to get instance of %s on host "%s"'
                    ' - falling back to CIM_ComputerSystem',
                    config.system_class_name, ns.connection.uri)
            get_computer_system._cs_cache[ns_path] = cs = \
                    ns.CIM_ComputerSystem.first_instance_name()
        LOG().debug('loaded instance instance of %s:%s for host "%s"',
            ns.name, cs.classname, ns.connection.uri)
    return get_computer_system._cs_cache[ns_path]
