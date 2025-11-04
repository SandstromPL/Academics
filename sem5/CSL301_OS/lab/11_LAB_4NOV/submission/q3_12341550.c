    #include <stdio.h>
    #include <pthread.h>
    #include <stdlib.h>
    #include <string.h>
    #include <unistd.h>

    #define MAX_LOGS 10

    char *log_buffer[MAX_LOGS];
    int count = 0;


    pthread_mutex_t buffer_lock = PTHREAD_MUTEX_INITIALIZER;
    pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER;
    pthread_cond_t not_full = PTHREAD_COND_INITIALIZER;

    void *worker(void *id) {
        for (int i = 0; i < 3; i++) {
            char msg[64];
            sprintf(msg, "Worker %ld message %d", (long)id, i);
            
            pthread_mutex_lock(&buffer_lock);
            while (count == MAX_LOGS)
                pthread_cond_wait(&not_full, &buffer_lock);
            
            log_buffer[count++] = strdup(msg);
            printf("Worker %ld queued log. (count=%d)\n", (long)id, count);

            pthread_cond_signal(&not_empty);
            pthread_mutex_unlock(&buffer_lock);
            usleep(100000); 
        }
        return NULL;
    }

    void *logger(void *arg) {
        FILE *f = fopen("log.txt", "w");
        if (!f) {
            perror("fopen");
            return NULL;
        }

        while (1) {

            pthread_mutex_lock(&buffer_lock);
            while (count == 0)
                pthread_cond_wait(&not_empty, &buffer_lock);
            
            char *msg = log_buffer[--count];

            pthread_cond_signal(&not_full);
            pthread_mutex_unlock(&buffer_lock);

            fprintf(f, "%s\n", msg);
            fflush(f);
            printf("Logger wrote: %s\n", msg);

            free(msg);
            usleep(50000); 
        }

        fclose(f);
        return NULL;
    }

    int main() {
        pthread_t log_thread, workers[3];
        pthread_create(&log_thread, NULL, logger, NULL);
        for (long i = 0; i < 3; i++)
            pthread_create(&workers[i], NULL, worker, (void *)i);

        for (int i = 0; i < 3; i++)
            pthread_join(workers[i], NULL);

        sleep(1);

        pthread_cancel(log_thread);
        pthread_join(log_thread, NULL);

        printf("\nAll workers finished. Check 'log.txt' for output.\n");
        return 0;
    }
