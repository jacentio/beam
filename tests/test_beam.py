import logging
import beam

def test_logger():
	b = beam.Beam()
	log = b.init_logger()
	assert isinstance(log, logging.Logger)
