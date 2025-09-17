#include "types.h"
#include "user.h"

#define PAGESIZE 4096
#define MAXPAGES 1024

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf(1, "Usage: tlbtest <numpages> <trials>\n");
        exit();
    }

    int numpages = atoi(argv[1]);
    int trials = atoi(argv[2]);

    if (numpages < 1 || numpages > MAXPAGES) {
        printf(1, "numpages out of range (1..%d)\n", MAXPAGES);
        exit();
    }

    int jump = PAGESIZE / sizeof(int);
    int i, t;

    int *arr = (int *)sbrk(numpages * PAGESIZE);
    if (arr == (void *)-1) {
        printf(1, "sbrk failed for %d pages\n", numpages);
        exit();
    }

    int pf_before = getpagefaults();

    uint start_ticks = uptime();

    for (t = 0; t < trials; t++) {
        for (i = 0; i < (numpages / 2) * jump; i += jump) {
            arr[i] += 1; // Access page to trigger page fault on first touch
        }
    }

    uint end_ticks = uptime();

    int pf_after = getpagefaults();

    printf(1, "Pages: %d\tTrials: %d\tTicks: %d\tPageFaults: %d\n",
           numpages, trials, end_ticks - start_ticks, pf_after - pf_before);

    exit();
}
