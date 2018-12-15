"""
Logger
"""

import time


class Logger:  # pylint: disable=too-many-instance-attributes
    """Logger"""

    def __init__(self):
        self.last_time_progress_logged = time.time()
        self.log_progress_every = 10  # seconds
        self.avg_processing_tempo = 0
        self.n_of_tempo_measures = 10
        self.last_processed = 0
        self.minimal_total_count = 50
        self.tx_cache_miss_count = 0
        self.tx_cache_length = 0

    def __getattr__(self, item):
        return self.log

    @staticmethod
    def log(*args):
        """log"""
        print('[{}] {}'.format(
            time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            args[0] if len(args) == 1 else args
        ))

    def log_processing(self, i, total):
        """log_processing"""
        if self._has_interval_passed() and self._is_enough_to_log(total):
            self.last_time_progress_logged = time.time()
            self.update_avg_processing_tempo(i)
            if i != self.last_processed:
                self.log('{0:.2f}% done, {1} left, txCache: {2}/{3}'.format(
                    100 * i / total,
                    self.get_time_left(i, total),
                    self.tx_cache_miss_count,
                    self.tx_cache_length,
                ))
                self.tx_cache_miss_count = 0
            self.last_processed = i

    def update_avg_processing_tempo(self, i):
        """update_avg_processing_tempo"""
        self.avg_processing_tempo = (
            (
                self.avg_processing_tempo * (self.n_of_tempo_measures - 1)
                + (i - self.last_processed) / self.log_progress_every
            ) / self.n_of_tempo_measures
        )

    def get_time_left(self, i, total):
        """get_time_left"""
        if self.avg_processing_tempo > 0:
            minutes, seconds = divmod(
                (total - i) / self.avg_processing_tempo, 60
            )
            hours, minutes = divmod(minutes, 60)
            return '%d:%02d:%02d' % (hours, minutes, seconds)
        return 'infinite'

    def register_tx_cache_miss(self):
        """register_tx_cache_miss"""
        self.tx_cache_miss_count += 1

    def register_cache_length(self, length):
        """register_cache_length"""
        self.tx_cache_length = length

    def _has_interval_passed(self):
        """_has_interval_passed"""
        return self._get_last_log_interval() > self.log_progress_every

    def _get_last_log_interval(self):
        """_get_last_log_interval"""
        return time.time() - self.last_time_progress_logged

    def _is_enough_to_log(self, total):
        """_is_enough_to_log"""
        return total > self.minimal_total_count
