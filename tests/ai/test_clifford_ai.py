# -*- coding: utf-8 -*-

# (C) Copyright 2024 IBM. All Rights Reserved.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Unit-testing clifford_ai"""
import pytest
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager

from qiskit_ibm_transpiler.ai.collection import CollectCliffords
from qiskit_ibm_transpiler.ai.synthesis import AICliffordSynthesis


def test_clifford_wrong_backend(random_circuit_transpiled, caplog):
    ai_optimize_cliff = PassManager(
        [
            CollectCliffords(),
            AICliffordSynthesis(backend_name="wrong_backend"),
        ]
    )
    ai_optimized_circuit = ai_optimize_cliff.run(random_circuit_transpiled)
    assert "couldn't synthesize the circuit" in caplog.text
    assert "Keeping the original circuit" in caplog.text
    assert (
        "User doesn't have access to the specified backend: wrong_backend"
        in caplog.text
    )
    assert isinstance(ai_optimized_circuit, QuantumCircuit)


@pytest.mark.skip(
    reason="Unreliable. It passes most of the times with the timeout of 1 second for the current circuits used"
)
def test_clifford_exceed_timeout(random_circuit_transpiled, backend, caplog):
    ai_optimize_cliff = PassManager(
        [
            CollectCliffords(),
            AICliffordSynthesis(backend_name=backend, timeout=1),
        ]
    )
    ai_optimized_circuit = ai_optimize_cliff.run(random_circuit_transpiled)
    assert "couldn't synthesize the circuit" in caplog.text
    assert "Keeping the original circuit" in caplog.text
    assert isinstance(ai_optimized_circuit, QuantumCircuit)


def test_clifford_wrong_token(random_circuit_transpiled, backend, caplog):
    ai_optimize_cliff = PassManager(
        [
            CollectCliffords(),
            AICliffordSynthesis(backend_name=backend, token="invented_token_2"),
        ]
    )
    ai_optimized_circuit = ai_optimize_cliff.run(random_circuit_transpiled)
    assert "couldn't synthesize the circuit" in caplog.text
    assert "Keeping the original circuit" in caplog.text
    assert "Invalid authentication credentials" in caplog.text
    assert isinstance(ai_optimized_circuit, QuantumCircuit)


@pytest.mark.disable_monkeypatch
def test_clifford_wrong_url(random_circuit_transpiled, backend, caplog):
    ai_optimize_cliff = PassManager(
        [
            CollectCliffords(),
            AICliffordSynthesis(backend_name=backend, base_url="https://ibm.com/"),
        ]
    )
    ai_optimized_circuit = ai_optimize_cliff.run(random_circuit_transpiled)
    assert "Internal error: 404 Client Error:" in caplog.text
    assert "Keeping the original circuit" in caplog.text


@pytest.mark.disable_monkeypatch
def test_clifford_unexisting_url(random_circuit_transpiled, backend, caplog):
    ai_optimize_cliff = PassManager(
        [
            CollectCliffords(),
            AICliffordSynthesis(
                backend_name=backend,
                base_url="https://invented-domain-qiskit-ibm-transpiler-123.com/",
            ),
        ]
    )
    ai_optimized_circuit = ai_optimize_cliff.run(random_circuit_transpiled)
    assert "couldn't synthesize the circuit" in caplog.text
    assert "Keeping the original circuit" in caplog.text
    assert (
        "Error: HTTPSConnectionPool(host='invented-domain-qiskit-ibm-transpiler-123.com', port=443):"
        in caplog.text
    )
    assert isinstance(ai_optimized_circuit, QuantumCircuit)


def test_clifford_function(random_circuit_transpiled, backend):
    ai_optimize_cliff = PassManager(
        [
            CollectCliffords(),
            AICliffordSynthesis(backend_name=backend),
        ]
    )
    ai_optimized_circuit = ai_optimize_cliff.run(random_circuit_transpiled)
    assert isinstance(ai_optimized_circuit, QuantumCircuit)
