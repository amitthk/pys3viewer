from pys3viewer.EMR import EMRProvider
from pys3viewer.Hadoop import HadoopProvider


class MapReduceProvider(object):
    """
    Factory Class - reates provider based on class name:
    """
    def factory(type):
        if type == "EMRProvider": return EMRProvider()
        if type == "HadoopProvider": return HadoopProvider()
        assert 0, "Bad provider name: " + type

    factory = staticmethod(factory)
