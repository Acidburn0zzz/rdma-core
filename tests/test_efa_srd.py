# SPDX-License-Identifier: (GPL-2.0 OR Linux-OpenIB)
# Copyright 2020 Amazon.com, Inc. or its affiliates. All rights reserved.

import errno
import pyverbs.enums as e
from pyverbs.pyverbs_error import PyverbsRDMAError
from tests.base import RDMATestCase
from tests.efa_base import SRDResources
import tests.utils as u
import unittest


class QPSRDTestCase(RDMATestCase):
    def setUp(self):
        super().setUp()
        self.iters = 100
        self.server = None
        self.client = None

    def create_players(self, send_ops_flags, qp_count=8):
        try:
            self.client = SRDResources(self.dev_name, self.ib_port, self.gid_index, send_ops_flags, qp_count)
            self.server = SRDResources(self.dev_name, self.ib_port, self.gid_index, send_ops_flags, qp_count)
        except PyverbsRDMAError as ex:
            if ex.error_code == errno.EOPNOTSUPP:
                raise unittest.SkipTest('Create SRD Resources is not supported')
            raise ex
        self.client.pre_run(self.server.psns, self.server.qps_num)
        self.server.pre_run(self.client.psns, self.client.qps_num)

    def test_qp_ex_srd_send(self):
        send_op = e.IBV_QP_EX_WITH_SEND
        self.create_players(send_op)
        u.traffic(self.client, self.server, self.iters, self.gid_index, self.ib_port,
                  new_send=True, send_op=send_op)

    def test_qp_ex_srd_send_imm(self):
        send_op = e.IBV_QP_EX_WITH_SEND_WITH_IMM
        self.create_players(send_op)
        u.traffic(self.client, self.server, self.iters, self.gid_index, self.ib_port,
                  new_send=True, send_op=send_op)
