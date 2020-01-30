from typing import Type

from .api import Spectrum, SpectrumReader, SpectrumWriter
from .options import Option
from .sampleidextraction import SampleIDExtraction


class Reader(SampleIDExtraction, SpectrumReader):
    """
    Reader for ADAMS spectra.
    """
    # Options
    separator = Option(help='the separator to use for identifying X and Y columns', default=';')

    def _read(self, specfile, fname):
        """
        Reads the spectra from the file handle.

        :param specfile: the file handle to read from
        :type specfile: file
        :param fname: the file being read
        :type fname: str
        :return: the list of spectra
        :rtype: list
        """
        sample_id = self.extract(fname)
        waves = []
        ampls = []
        for line in specfile.readlines():
            line = line.strip()
            if len(line) == 0:
                continue

            parts = line.split(self.separator)

            waves.append(float(parts[0]))
            ampls.append(float(parts[1]))

        return [Spectrum(sample_id, waves, ampls)]

    def binary_mode(self, filename: str) -> bool:
        return False

    @classmethod
    def get_writer_class(cls) -> 'Type[Writer]':
        return Writer


class Writer(SpectrumWriter):
    """
    Writer for ADAMS spectra.
    """
    # Options
    separator = Option(help='the separator to use for identifying X and Y columns', default=';')

    def _write(self, spectra, specfile, as_bytes):
        """
        Writes the spectra to the filehandle.

        :param spectra: the list of spectra
        :type spectra: list
        :param specfile: the file handle to use
        :type specfile: file
        """
        if len(spectra) != 1:
            raise ValueError("Can only write a single spectrum")

        spectrum = spectra[0]

        for wave, ampl in reversed(list(zip(spectrum.waves, spectrum.amplitudes))):
            specfile.write(f"{wave}{self.separator}{ampl}\n")

    def binary_mode(self, filename: str) -> bool:
        return False

    def get_reader_class(cls) -> Type[Reader]:
        return Reader


read = Reader.read


write = Writer.write
