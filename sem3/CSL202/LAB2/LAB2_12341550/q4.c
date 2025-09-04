#include<stdio.h>
#include<stdlib.h>

struct Node{
	int data;
	struct Node * next;

};

void insertAtHead(struct Node ** head,int data){

	struct Node * temp = (struct Node *)malloc(sizeof(struct Node));
	temp -> data = data;
	temp -> next = NULL;
	
	if(*head == NULL){
		*head = temp;	
	}else{
		temp -> next = *head;
		*head = temp;	
	}
}

void insertAtTail(struct Node ** head,int data){

	struct Node * temp = (struct Node *)malloc(sizeof(struct Node));
	temp -> data = data;
	temp -> next = NULL;
	
	if(*head == NULL){
		*head = temp;	
	}else{
		struct Node * curr = *head;
		while(curr -> next != NULL){
			curr = curr -> next;	
		}
		curr -> next = temp;		
	}
}

 // postion >= 2
void insertingBetween(struct Node ** head,int data,int position){

	struct Node * temp = (struct Node *)malloc(sizeof(struct Node));
	temp -> data = data;
	temp -> next = NULL;
	int cnt = 1;
	struct Node * prev = *head;
	while(cnt < position - 1){
		prev = prev -> next;
		cnt++;
	}
	temp -> next = prev -> next;
	prev -> next = temp;
}

void deletion(struct Node ** head,int position){
	
	struct Node * prev = *head;
	if(position == 1){ 	 // position == 1
		prev = prev -> next;
		*head = prev;		
	}else{                  //position >= 2
		int cnt = 1;
		while(cnt < position - 1 && prev != NULL){
			prev = prev -> next;
			cnt++;
		}
		if(prev == NULL){
			printf("Position not found .\n");		
		}else{
			prev -> next = prev -> next -> next;		
		}	
	}
}

void print(struct Node** head){

	struct Node * temp = *head;
	if(temp == NULL){
		printf("List is empty .\n");	
	}else{
		while(temp != NULL){
			printf("%d ",temp -> data);
			temp = temp -> next;		
		}	
	}

}


int main(){

	struct Node * node = NULL;
	insertAtHead(&node,2);
	insertAtHead(&node,6);
	insertAtTail(&node,3);
	insertAtTail(&node,10);
	print(&node);
	printf("\n ");
	insertingBetween(&node,21,3);
	print(&node);
	printf("\n ");
	deletion(&node,5);
	print(&node);
	printf("\n ");

}
