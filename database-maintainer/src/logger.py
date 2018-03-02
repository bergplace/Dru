import time


class Logger(object):

    def __init__(self):
        self.last_time_progress_logged = time.time()
        self.log_progress_every = 5  # seconds
        self.avg_processing_tempo = 0
        self.n_of_tempo_measures = 10
        self.last_processed = 0

    @staticmethod
    def log(msg):
        print('[db-maintainer][{}] {}'.format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            msg
        ))

    def log_processing(self, i, total):
        if time.time() - self.last_time_progress_logged > self.log_progress_every:
            self.last_time_progress_logged = time.time()
            self.update_avg_processing_tempo(i, total)
            self.log('processing done in {0:.4f}%, {1} left'.format(
                i / total,
                self.get_time_left(total)
            ))
            self.last_processed = i

    def update_avg_processing_tempo(self, i, total):
        self.avg_processing_tempo = ((
            (self.avg_processing_tempo * (self.n_of_tempo_measures - 1) /
             self.n_of_tempo_measures)
            + (i - self.last_processed) / self.n_of_tempo_measures)
            / self.log_progress_every)

    def get_time_left(self, total):
        m, s = divmod(total / self.avg_processing_tempo, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

