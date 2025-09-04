#include<stdio.h>
int main(){
	int n;
	scanf("%d",&n);
	int m[n][n];
	int N[n][n];
	int p[n][n];
	for(int i=0;i<n;i++){
		for(int j=0;j<n;j++){+
			scanf("%d",&m[i][j]);
		}
	}
	for(int i=0;i<n;i++){
                for(int j=0;j<n;j++){+
                        scanf("%d",&N[i][j]);
                }
        }
	for(int i=0;i<n;i++){

		for(int j=0; j<n;j++){
			p[i][j]=0;
			for(int k=0;k<n;k++){
				p[i][j]+=m[i][k]*N[k][j];
			}
		}
	}
	for(int i=0;i<n;i++){
                for(int j=0;j<n;j++){+
                        printf("%d\t",p[i][j]);
                }
		printf("\n");
        }
	return 0;
}

			
