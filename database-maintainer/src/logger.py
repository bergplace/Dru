import time


class Logger(object):

    def __init__(self):
        self.last_time_progress_logged = time.time()
        self.log_progress_every = 10  # seconds
        self.avg_processing_tempo = 0
        self.n_of_tempo_measures = 10
        self.last_processed = 0
        self.minimal_total_count_to_bother_logging = 50

    @staticmethod
    def log(msg):
        print('[db-maintainer][{}] {}'.format(
            time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            msg
        ))

    def log_processing(self, i, total):
        if time.time() - self.last_time_progress_logged > self.log_progress_every\
                and total > self.minimal_total_count_to_bother_logging:
            self.last_time_progress_logged = time.time()
            self.update_avg_processing_tempo(i)
            self.log('processing done in {0:.2f}%, {1} left'.format(
                100 * i / total,
                self.get_time_left(i, total)
            ))
            self.last_processed = i

    def update_avg_processing_tempo(self, i):
        self.avg_processing_tempo = (
            (
                self.avg_processing_tempo * (self.n_of_tempo_measures - 1)
                + (i - self.last_processed) / self.log_progress_every
            ) / self.n_of_tempo_measures
        )

    def get_time_left(self, i, total):
        if self.avg_processing_tempo > 0:
            m, s = divmod((total - i) / self.avg_processing_tempo, 60)
            h, m = divmod(m, 60)
            return '%d:%02d:%02d' % (h, m, s)
        else:
            return 'infinite'

