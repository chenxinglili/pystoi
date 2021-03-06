import pytest
import matlab.engine
import numpy as np
import scipy
from numpy.testing import assert_allclose
from pystoi.stoi import stoi
from pystoi.stoi import FS, N_FRAME, NFFT, NUMBAND, MINFREQ, N, BETA, DYN_RANGE

RTOL = 1e-6
ATOL = 1e-6

eng = matlab.engine.start_matlab()
eng.cd('matlab/')


def test_stoi_good_fs():
    x = np.random.randn(2*FS, )
    y = np.random.randn(2*FS, )
    stoi_out = stoi(x, y, FS)
    x_m = matlab.double(list(x))
    y_m = matlab.double(list(y))
    stoi_out_m = eng.stoi(x_m, y_m, float(FS))
    assert_allclose(stoi_out, stoi_out_m, atol=ATOL, rtol=RTOL)


def test_estoi_good_fs():
    x = np.random.randn(2*FS, )
    y = np.random.randn(2*FS, )
    estoi_out = stoi(x, y, FS, extended=True)
    x_m = matlab.double(list(x))
    y_m = matlab.double(list(y))
    estoi_out_m = eng.estoi(x_m, y_m, float(FS))
    assert_allclose(estoi_out, estoi_out_m, atol=ATOL, rtol=RTOL)


def test_stoi_downsample():
    """ FAILING BECAUSE OF RESAMPLING """
    for fs in [11025, 16000, 22050, 32000, 44100, 48000]:
        x = np.random.randn(2*fs, )
        y = np.random.randn(2*fs, )
        stoi_out = stoi(x, y, fs)
        x_m = matlab.double(list(x))
        y_m = matlab.double(list(y))
        stoi_out_m = eng.stoi(x_m, y_m, float(fs))
        assert_allclose(stoi_out, stoi_out_m, atol=ATOL, rtol=RTOL)


def test_stoi_upsample():
    """ FAILING BECAUSE OF RESAMPLING """
    for fs in [8000]:
        x = np.random.randn(2*fs, )
        y = np.random.randn(2*fs, )
        stoi_out = stoi(x, y, fs)
        x_m = matlab.double(list(x))
        y_m = matlab.double(list(y))
        stoi_out_m = eng.stoi(x_m, y_m, float(fs))
        assert_allclose(stoi_out, stoi_out_m, atol=ATOL, rtol=RTOL)


def test_stoi_matlab_resample():
    from pystoi.stoi import FS
    import matlab_wrapper
    matlab = matlab_wrapper.MatlabSession()
    matlab.workspace.cd('matlab/')
    matlab.put('FS', float(FS))
    for fs in [8000, 11025, 16000, 22050, 32000, 44100, 48000]:
        matlab.put('fs', float(fs))
        x = np.random.randn(2*fs,)
        y = np.random.randn(2*fs, )
        matlab.put('x', x)
        matlab.put('y', y)
        matlab.eval('x_r = resample(x, FS, fs)')
        matlab.eval('y_r = resample(y, FS, fs)')
        x_r = matlab.get('x_r')
        y_r = matlab.get('y_r')
        stoi_out = stoi(x_r, y_r, FS)
        stoi_out_m = matlab.eval('stoi_out_m = stoi(x_r, y_r, FS)')
        assert_allclose(stoi_out, matlab.get('stoi_out_m'), atol=ATOL, rtol=RTOL)


"""
Conclusion :
    The source of difference between the original Matlab and this STOI is the
    resampling method which uses different filters and interpolations.
    However, informal tests with actual speech files produce very similar results
    for both implementations.
"""

if __name__ == '__main__':
    pytest.main([__file__])
