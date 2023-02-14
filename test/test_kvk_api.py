
"""
An example test case with unittest.
See: https://docs.python.org/3/library/unittest.html
"""
from kvk.src.kvk import KVK
from kvk.src.kvk import BasisProfielPaths

KVK_NUMBER = '68750110'
VESTIGINGSNUMMER = '000038509504'

kvk = KVK(test=True)


def test_get_basis_profile():
    response = kvk.get_basis_profiel(KVK_NUMBER)
    assert response.status_code == 200

    response = kvk.get_basis_profiel(KVK_NUMBER, BasisProfielPaths.vestigingen)
    assert response.status_code == 200

    response = kvk.get_basis_profiel(KVK_NUMBER, BasisProfielPaths.eigenaar)
    assert response.status_code == 200

    response = kvk.get_basis_profiel(
        KVK_NUMBER, BasisProfielPaths.hoodfvestiging)
    assert response.status_code == 200


def test_get_vestigingsprofiel():
    response = kvk.get_vestigingsprofiel(VESTIGINGSNUMMER)
    assert response.status_code == 200


def test_get_companies():
    response = kvk.get_companies(kvk_number=KVK_NUMBER)
    assert response.status_code == 200


def test_get_naamgevingen():
    response = kvk.get_naamgevingen(kvk_number=KVK_NUMBER)
    assert response.status_code == 200
