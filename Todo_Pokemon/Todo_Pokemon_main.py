#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <Windows.h>
#include <time.h>

#pragma warning(disable:4996)

#define LINE1 "=================================="
#define LINE2 "----------------------------------"
#define MAX 50
#define Text_MAX 256

/*
<일정 관리 프로그램> => 동기부여 가능하게 
>> 파일 시스템 

>>구현할 기능

0. 메인에 보일 화면 

- 메인 타이틀 / 오늘 날짜 
- 오늘의 일정 / <중요 일정> 
- 오늘의 일정
- 오늘의 할 일 
- 다가오는 일정 -- 급한 일정들 D-d 표시로 
- start 

1. 해야 할 일 보여주기 & 일정 보여주기 
	- 오늘 날짜 단위
	- 주 단위
	- 전체 목록 

2. 할 일 추가하기 - 구조체 / 카테고리, 이름 , 완료 여부 , 기한 , 중요도 (이모티콘 호환 ★)
3. 일정 추가하기 - 구조체 / 카테고리, 이름, 기한 , 기한 표시 여부 , 중요도 
4. 관리 - 삭제 , 수정 

5. 완료 된 할 일 보기 

6. 저장 


<박물관 상점>

1. 포켓몬 가챠  
2. 포켓몬 아이템(진화) 
3. 도감 

<박물관>

1. 포켓몬 전시
2. 명성도
3. 스테이터스 확인 


*/



typedef struct todo {

	char category[50];
	char name[Text_MAX];
	int done;
	int date;
	int level;
	int used;

}TODO;

typedef struct schedule {

	char category[50];
	char name[Text_MAX];
	int done;
	int date;
	int level;

}DAY;

typedef struct wallet {

	int money;
	int point;
	int w_level;

}WALLET;


typedef struct Pokemon {

	int number;
	char name_1[25];
	char name_2[25];
	char name_3[25];

	char type[20];
	int type_num;
	int level;

	int total;


}POKEMON;

typedef struct Book {

	int sum;
	

};


typedef struct Item {

	struct Pokemon* My_Pokemon;
	int P_token[12];


}ITEM;

time_t timer;
struct tm* t;

void Menu(struct tm* t, struct wallet* my_money);
void reset();
void Print(TODO* list, int cnt_file[2]);
void Print_all(TODO* list, int cnt_file[2]);
TODO* setup_list(int cnt_file[2]); // 처음 읽는 작업 - 리스트
struct wallet* setup_money(); //처음 읽는 작업 - 돈
struct item* setup_item(); //처음 읽는 작업 - 아이템

//Todo
/*-------------------------------------------------------------*/
TODO* Add_todo(TODO* list, int cnt_file[2]); // 투두 만들기
void Save_File(TODO* list, int cnt_file[2], WALLET* my_money, ITEM* my_item); //파일 세이브 
void Delete_todo(TODO* list, int cnt_file[2]); // 투두 지우기 
void Check_Todo(TODO* list, int cnt_file[2], struct wallet *my_money); //투두 체크 

//Pokemon Park
/*-------------------------------------------------------------*/
void Pokemon_Menu(WALLET* my_money, ITEM* my_item);
void Get_Money(WALLET* my_money, ITEM* my_item);
void Item_store(struct Item* my_Item, struct wallet* my_wallet);
void Get_pokemon(struct Item* my_item, struct wallet* my_wallet);
void My_pokemon(ITEM* my_item, WALLET* my_money);
void Show_pokemon(ITEM* my_item, WALLET* my_money, int index);

int main(){

	//오늘 시간 불러오기 
	timer = time(NULL);
	t = localtime(&timer);

	//랜덤 호출 
	srand(time(NULL));


	//wallet
	struct wallet *my_money = NULL;

	//item
	struct item* my_item = NULL;


	int cnt_file[2] = { 0,0 }; // 투두, 일정의 갯수 카운트 배열 
	int choice = -1;

	TODO* list = NULL;
	
	//프로그램 시작 시 파일 읽으며 시작 
	list = setup_list(cnt_file);
	my_money = setup_money();
	my_item = setup_item();
	int cnt_todo = 1;

	while (1)
	{
		system("cls");
		Menu(t, my_money);
		scanf("%d", &choice);


		switch(choice)
		{

		case 0: 
			exit(main);

		case 1:
			Print_all(list,cnt_file);
			break;
		case 2:
			list = Add_todo(list,cnt_file);
			break;
		case 3:
			Check_Todo(list, cnt_file, my_money);
			break;
		case 4:
			Delete_todo(list, cnt_file);
			break;

		case 5:
			Save_File(list, cnt_file, my_money, my_item);
			break;

		case 6:
			Pokemon_Menu(my_money, my_item);
			break;



		}



	}








	return 0;
}

TODO* setup_list(int cnt_file[2]) {

	char tmp[MAX][Text_MAX]; //잠시 담을 임시 저장소
	int cnt = 0;
	char* token = NULL;
	char* box[5] = { NULL }; //구조체 옮기기 전 잠시 넣을 곳 

	FILE* input = fopen("current_list.txt", "r");
	
	if (input == NULL)
	{
		printf("파일 열기를 실패하였습니다.\n");
	}

	fscanf(input, "%d", &cnt);
	fscanf(input, "%*c");

	cnt_file[0] = cnt; //배열에 옮겨주기 


	TODO* list = (struct todo*)malloc(sizeof(struct todo) * cnt);

	for(int i=0; i<cnt; i++)
	{
		fgets(tmp[i], 256, input);
		fscanf(input, "%d", &list[i].done);
		fscanf(input, "%d", &list[i].date);
		fscanf(input, "%d", &list[i].level);
		fscanf(input, "%*c");
		if (list[i].done == 1)
		{
			list[i].used = 1;
		}
		else
			list[i].used = 0;
	}




	for (int i = 0; i < cnt; i++)
	{
		token = strtok(tmp[i], "__");

		for (int j = 0; j < 2; j++)
		{
			box[j] = token;
			token = strtok(NULL, "__");
		}

		strcpy(list[i].category, box[0]);
		strcpy(list[i].name, box[1]);
		token = NULL;
	}

	fclose(input);
	return list;
}

struct wallet* setup_money() {

	struct wallet *list =NULL;

	list = (WALLET*)malloc(sizeof(WALLET));

	FILE* input = fopen("money.txt", "r");

	if (input == NULL)
	{
		printf("파일 열기 실패");
		return;
	}

	fscanf(input, "%d", &list->money);
	fscanf(input, "%d", &list->point);
	fscanf(input, "%d", &list->w_level); 


	fclose(input);
	return list;


}

struct item* setup_item()
{
	int pokemon=0; //포켓몬 수
	char* token = NULL;
	char tmp[100]; //잠시 담을 임시 저장소
	char* box[4]; // 구조체 옮기기 전


	//------------------------------

	ITEM* list = NULL;

	list = (ITEM*)malloc(sizeof(ITEM));

	FILE* input = fopen("item.txt", "r");

	if (input == NULL)
	{
		printf("파일 열기 실패");
		return;
	}

	for (int i = 0; i < 12; i++)
	{
		fscanf(input, "%d", &list->P_token[i]);
	}

	fclose(input);

	/*-----------------------------------*/

	FILE* p_input = fopen("my_pokemon.txt","r");

	fscanf(p_input, "%d", &pokemon);

	list->My_Pokemon = (POKEMON*)malloc(sizeof(POKEMON) * pokemon);

	fscanf(p_input, "%*c");

	for (int i = 0; i < pokemon; i++)
	{
		fscanf(p_input, "%d", &list->My_Pokemon[i].number); //고유넘버
		fscanf(p_input, "%*c");
		fgets(tmp, 100, p_input);
		token = strtok(tmp, " ");

		for (int j = 0; j < 4; j++)
		{
			box[j] = token;
			token = strtok(NULL, " ");
		}

		strcpy(list->My_Pokemon[i].name_1, box[0]);
		strcpy(list->My_Pokemon[i].name_2, box[1]);
		strcpy(list->My_Pokemon[i].name_3, box[2]);
		strcpy(list->My_Pokemon[i].type, box[3]);

		fscanf(p_input, "%d", &list->My_Pokemon[i].type_num);
		fscanf(p_input, "%d", &list->My_Pokemon[i].level);

		fscanf(p_input, "%*c");

		list->My_Pokemon[i].total = pokemon;

		/*
		저장 예시
		1 :: 총 수

		13 :: 고유넘버
		이름1 이름2 이름3
		3 :: 레벨
		10 :: 타입
		
		...

		*/


	}

	fclose(p_input);

	return list;

}


void Menu(struct tm * t, struct wallet *my_money) {

	char day[][10] = {"일", "월", "화", "수", "목", "금", "토"};

	char today[10] = { NULL };

	strcpy(today, day[t->tm_wday]);
	

	printf("\n");
	printf("		Todo List Program     v.0.0\n");
	printf("		================================\n");
	printf("		%d-%d-%d (%s)\n",
					t->tm_year+1900,t->tm_mon+1,t->tm_mday, today);
	printf("		Money : %d\n", my_money->money);
	printf("		Point : %d\n", my_money->point);
	printf("		--------------------------------\n");
	printf("		◎ 1. Show List (Current)\n");
	printf("		◎ 2. Add Todo\n");
	printf("		◎ 3. Check Todo\n");
	printf("		◎ 4. Delete\n");
	printf("		◎ 5. Save all\n");
	printf("		--------------------------------\n");
	printf("		◎ 6. Pokemon Park\n");
	printf("		--------------------------------\n");
	printf("		◎ 0. EXIT\n");
	printf("		--------------------------------\n");
	printf("		Choose >> ");

}

void reset()
{
	int reset = -1;
	printf("\n\nPress any number... >> ");
	scanf("%d", &reset);

}


void Print(TODO *list, int cnt_file[2])
{
	

	system("cls");
	
	printf("L I S T\n\n");
	printf(":: Name   \n");
	printf("================================================================\n");
	


	for (int i = 0; i < cnt_file[0]; i++)
	{
		printf("%d) %s  \t%-20s  \t",i+1, list[i].category, list[i].name);
		printf("%d\t", list[i].date);

		if (list[i].done== 0) printf("□\n");
		else if (list[i].done == 1) printf("■\n");

	}

	

}

void Print_all(TODO* list, int cnt_file[2]) {

	Print(list, cnt_file);

	reset();



}



TODO* Add_todo(TODO *list, int cnt_file[2]) {
	
	

	system("cls");
	
	int count = cnt_file[0];
	
	cnt_file[0] = cnt_file[0] + 1;

	list = (struct todo*)realloc(list,sizeof(struct todo) * cnt_file[0]);

	printf("\nADD LIST");
	printf("=======================================\n");
	printf("Todo category : ");

	scanf("%*c");

	gets(list[count].category);

	printf("\nTodo name : ");

	gets(list[count].name);

	printf("\nTodo date :");
	
	scanf("%d", &list[count].date);
	

	printf("\nTodo level :");

	scanf("%d", &list[count].level);

	list[count].done = 0;
	list[count].used = 0;

	reset();

	return list;

}

void Save_File(TODO* list, int cnt_file[2], WALLET *my_money, ITEM* my_item)
{

	/*Save TODO-----------------------------------*/
	char tmp[Text_MAX];

	FILE* output;

	output = fopen("current_list.txt", "w+");


	fprintf(output, "%d\n", cnt_file[0]); 
	//현재 카운트 개수


	for (int i = 0; i < cnt_file[0]; i++)
	{	
		
		fprintf(output, "%s__%s__\n%d %d %d\n",
			 list[i].category, list[i].name, list[i].done, list[i].date, list[i].level);
		
		
		

	}

	fclose(output);

	/*Save Wallet-----------------------------------*/

	FILE* output_m = fopen("money.txt", "w");
	fprintf(output_m, "%d\n", my_money->money);
	fprintf(output_m, "%d\n", my_money->point);
	fprintf(output_m, "%d\n", my_money->w_level);
	fclose(output_m);

	/*Save Items*/

	FILE* output_I = fopen("item.txt", "w");
	for (int i = 0; i < 12; i++)
	{
		fprintf(output_I, "%d\n", my_item->P_token[i]);
	}
	fclose(output_I);

	FILE* output_P = fopen("my_pokemon.txt", "w");

	fprintf(output_P, "%d\n", my_item->My_Pokemon[0].total);
	fprintf(output_P, "\n");

	for (int i = 0; i < my_item->My_Pokemon[0].total; i++)
	{
		fprintf(output_P, "%d\n", my_item->My_Pokemon[i].number);
		fprintf(output_P, "%s %s %s %s", my_item->My_Pokemon[i].name_1,
			my_item->My_Pokemon[i].name_2, my_item->My_Pokemon[i].name_3,
			my_item->My_Pokemon[i].type);
		fprintf(output_P, "%d\n", my_item->My_Pokemon[i].type_num);
		fprintf(output_P, "%d\n", my_item->My_Pokemon[i].level);
		fprintf(output_P,"\n");
	}

	fclose(output_P);
	
	


	//안내 메세지 코드
	printf("\n		Save successed!\n");
	int reset = -1;
	printf("\n		Press any number... >> ");
	scanf("%d", &reset);
	
}

void Delete_todo(TODO* list, int cnt_file[2])
{
	int choice = -1;

	system("cls");
	Print(list, cnt_file);

	printf("------------------------------------------\n");
	printf("# if you want to go back, press 0\n");
	printf("# Press the number you want to delete... >> ");


	scanf("%d", &choice);
	if (choice == 0) reset();
	
	else if (choice > cnt_file[0])
	{
		printf("\n\n# There's no number in the list... ");
		reset();
	}
	
	else {
		
		for (int i = choice - 1; i < cnt_file[0] - 1; i++)
		{
			memcpy(&list[i], &list[i + 1], sizeof(TODO));

		}

		cnt_file[0] = cnt_file[0] - 1;

		printf("\nDelete successed...");
		reset();



	}
	


}

void Check_Todo(TODO* list, int cnt_file[2], struct wallet *my_money)
{
	int n;
	int choice;
	int level_p;
	system("cls");

	Print(list,cnt_file);

	printf("Press the number you want to check >> ");
	scanf("%d", &n);

	if (list[n - 1].done == 0&&list[n-1].used !=1)
	{
		list[n - 1].done = 1;
		list[n - 1].used = 1;
		level_p = list[n - 1].level;
		my_money->point += level_p;
	}
	else 
	{
		list[n - 1].done = 0;
	}


	system("cls");
	Print(list, cnt_file);


	printf("\nSuccess!\nPress 1 : continue check / Press 0 : back to Menu >> ");
	scanf("%d", &choice);
	if (choice == 1) Check_Todo(list, cnt_file, my_money);
	else
	{
		return;
	}

	


}

void Pokemon_Menu(WALLET *my_money, ITEM *my_item){

	int n=0;

	system("cls");
	

	printf("\n");
	printf("		Welcome to the Pokemon park!\n");
	printf("		===============================\n");
	printf("		[Current]\n");
	printf("		Point : %d\n", my_money->point);
	printf("		Money : %d\n", my_money->money);
	printf("		===============================\n");
	printf("		▶ 1) Point Exchange\n");
	printf("		-------------------------------\n");
	printf("		▶ 2) Get Pokemon (Point)\n\n");
	printf("		▶ 3) Pokemon Item Store (Money)\n");
	printf("		-------------------------------\n");
	printf("		▶ 4) My Pokemon & Item\n");
	printf("		-------------------------------\n");
	printf("		▶ 5) Go to Pokemon Park\n\n");
	printf("		▶ 0) Back to Menu\n");
	printf("		===============================\n");
	printf("		Press key ... >> ");

	

	scanf("%d", &n);

	switch (n) 
	{
	case 1:
		Get_Money(my_money,my_item);
		break;

	case 2:
		Get_pokemon(my_item, my_money);
		break;
		
	case 3:
		Item_store(my_item, my_money);
		break;

	case 4:
		My_pokemon(my_item, my_money);
		break;

	case 5:
		//go pokemon park
		break;

	case 0:
		break;
	}

}

void Get_Money(WALLET* my_money, ITEM* my_item) {
	
	system("cls");

	printf("	\n	Exchange Point\n");
	printf("	=========================================\n");
	printf("	Current Point : %d\n", my_money->point);
	printf("	Current Money : %d\n", my_money->money);
	printf("	-----------------------------------------\n");
	printf("	▶ 1) Point -> Money exchange\n");
	printf("	▶ 0) Go to menu\n");
	printf("	-----------------------------------------\n");
	printf("	Press key... >> ");

	int n;

	scanf("%d", &n); 
	if (n == 1) 
	{
		system("cls");

		printf("	\n	Exchange Point\n");
		printf("	=========================================\n");
		printf("	Current Point : %d\n", my_money->point);
		printf("	Current Money : %d\n", my_money->money);
		printf("	-----------------------------------------\n");
		printf("	▶ 1) Point -> Money exchange\n");
		printf("	▶ 0) Go to menu\n");
		printf("	-----------------------------------------\n");

		printf("\n");
		printf("	::How many Point >> ");

		int much=0;

		scanf("%d", &much);

		if (much > my_money->point)
		{
			printf("	* You don't have enough point\n");
			printf("	* Press any key >> ");

			scanf("%d", &much);
			Get_Money(my_money, my_item);

		}

		my_money->money = much*100;
		my_money->point -= much;
		
		system("cls");
		Get_Money(my_money, my_item);
	}

	else if (n == 0)
	{
		Pokemon_Menu(my_money,my_item);
	}


}

void Get_pokemon(struct Item* my_item, struct wallet* my_wallet)
{
	char type_name[13][20] = { "고스트", "노말", "물", "바위", "벌레", "불",
							"비행", "얼음", "에스퍼", "전기", "페어리", "풀", "희귀"};

	system("cls");

	printf("	\n	Get Pokemon!\n");
	printf("	:: You can get random Pokemon\n");
	printf("	=========================================\n");
	printf("	Current Point : %d\n", my_wallet->point);
	printf("	-----------------------------------------\n");
	printf("	▶ 1) Get Normal Pokemon\n");
	printf("	▶ :: 1 try = 3 Point\n\n");

	printf("	▶ 2) Get Rare Pokemon\n");
	printf("	▶ :: 1 try = 10 Point\n\n");

	printf("	▶ 0) Go to menu\n");
	printf("	-----------------------------------------\n");
	printf("	Press key... >> ");

	int n;
	int losing_point = my_wallet->point;

	scanf("%d", &n);

	if (n == 1)
	{
		int random;
		srand(time(NULL));
		random = rand() % 64;
		random += 13;
		

		//중복시 토큰으로 교환
		for (int i = 0; i < my_item->My_Pokemon[0].total; i++)
		{
			if (random == my_item->My_Pokemon[i].number)
			{
				system("cls");
				printf("\n\n");
				printf("	=========================================\n");
				printf("	★ You found ....\n");
				printf("	★ [%s] !!\n\n", my_item->My_Pokemon[i].name_1);
				printf("	:::: You already have this Pokemon, So\n");
				printf("	:::: [%s] token plus one!\n", my_item->My_Pokemon[i].type);
				printf("	-----------------------------------------\n");
				printf("	Press any key... >> ");

				my_wallet->point = losing_point - 3;

				my_item->P_token[my_item->My_Pokemon[i].type_num]++;
				int key;
				scanf("%d", &key);

				Get_pokemon(my_item, my_wallet);
				
			}
		}

		FILE* input_N = fopen("pokemon_list.txt", "r");

		char buf[3];
		char tmp[50];
		char* p;
		int line;
		char* token;
		char* box[4];
		int plus =0;

		sprintf(buf, "%d", random);

		while (fscanf(input_N,"%s",&tmp)!= EOF)
		{
			p = strstr(tmp, buf);
			if (p != NULL)
			{
				line = strlen(tmp) - (p - tmp) + 1;
				fseek(input_N, (-1) * line, SEEK_CUR); //해당 위치로 커서 이동
				
				plus = my_item->My_Pokemon[0].total;
				realloc(my_item->My_Pokemon, sizeof(POKEMON) * (plus + 1));

				fscanf(input_N, "%d", &my_item->My_Pokemon[plus].number);
				fscanf(input_N, "%*c");
				
				
				fgets(tmp, 50, input_N);

				token = strtok(tmp, " ");

				for (int j = 0; j < 4; j++)
				{
					box[j] = token;
					token = strtok(NULL, " ");
				}

				strcpy(my_item->My_Pokemon[plus].name_1, box[0]);
				strcpy(my_item->My_Pokemon[plus].name_2, box[1]);
				strcpy(my_item->My_Pokemon[plus].name_3, box[2]);
				strcpy(my_item->My_Pokemon[plus].type, box[3]);

				fscanf(input_N, "%d", &my_item->My_Pokemon[plus].type_num);

				my_item->My_Pokemon[plus].level = 1;
				my_item->My_Pokemon[plus].total = plus + 1;
				my_item->My_Pokemon[0].total = plus + 1;

				
				fclose(input_N);
				break;
			}
		}

		//fclose(input_N);

		my_wallet->point = losing_point-3;

		system("cls");

		printf("\n");
		printf("	=========================================\n");
		printf("	★ You found ....\n");
		printf("	★ [%s] !!\n\n", my_item->My_Pokemon[plus].name_1);
		printf("	:::: New Pokemon, Congratulations!!\n");
		printf("	-----------------------------------------\n");
		printf("	Press any key... >> ");

		int key;
		scanf("%d", &key);

		

		Pokemon_Menu(my_wallet, my_item);
		
		//fclose(input_N);
	}


}

void Item_store(struct Item* my_Item, struct wallet* my_wallet) {

	system("cls");

	printf("	\n	Item Store!\n");
	printf("	:: You can get random Pokemon Token\n");
	printf("	:: Token can makes your Pokemon Grow!\n");
	printf("	=========================================\n");
	printf("	Current Money : %d\n", my_wallet->money);
	printf("	-----------------------------------------\n");
	printf("	▶ 1) Buy random Pokemon Token\n");
	printf("	▶ :: Token = 100$ \n");
	printf("	▶ 0) Go to menu\n");
	printf("	-----------------------------------------\n");
	printf("	Press key... >> ");

	int n;

	int random_token;
	char token_type[20] = " ";

	scanf("%d", &n);

	/*
	0. 고스트
	1. 노말
	2. 물
	3. 바위
	4. 벌레
	5. 불
	6. 비행
	7. 얼음
	8. 에스퍼
	9. 전기
	10. 페어리
	11. 풀
	12. 희귀/전설/환상
	*/

	char type_name[12][20] = { "고스트", "노말", "물", "바위", "벌레", "불",
							"비행", "얼음", "에스퍼", "전기", "페어리", "풀" };

	if (n == 1)
	{
		if (my_wallet->money < 100)
		{
			printf("	You don't have enough money!\n");
			printf("	Press any key... >> ");

			int key;
			scanf("%d", &key);
			Pokemon_Menu(my_wallet, my_Item);

		}

		random_token = rand() % 11; //포켓몬 타입 12가지

		for (int i = 0; i < 12; i++)
		{
			if (random_token == i)
			{
				my_Item->P_token[i]++;
				my_wallet->money -= 100;
			}
		}

		system("cls");
		printf("	\n	Item Store!\n");
		printf("	:: You can get random Pokemon Token\n");
		printf("	:: Token can makes your Pokemon Grow!\n");
		printf("	=========================================\n");
		printf("	★ You got ....\n");
		printf("	★ [%s] type token!!\n", type_name[random_token]);
		printf("	-----------------------------------------\n");
		
		printf("	Press any key... >> ");

		scanf("%d", &n);

		Item_store(my_Item, my_wallet);

	}

	else if (n == 0)
	{
		Pokemon_Menu(my_wallet, my_Item);
	}



}

void My_pokemon(ITEM* my_item, WALLET* my_money)
{

	char type_name[12][20] = { "고스트", "노말", "물", "바위", "벌레", "불",
							"비행", "얼음", "에스퍼", "전기", "페어리", "풀"};

	system("cls");

	printf("\n");
	printf("	My Pokemon & Item\n");
	printf("	==============================================\n");
	printf("	[TOKEN ITEM] :: for grow up your pokemon\n");
	printf("	::고스트: %-3d\t노말: %-3d\t물: %-3d\n",
				my_item->P_token[0], my_item->P_token[1], my_item->P_token[2]);
	printf("	::바위: %-3d\t벌레: %-3d\t불: %-3d\n",
				my_item->P_token[3], my_item->P_token[4], my_item->P_token[5]);
	printf("	::비행: %-3d\t얼음: %-3d\t에스퍼: %-3d\n",
				my_item->P_token[6], my_item->P_token[7], my_item->P_token[8]);
	printf("	::전기: %-3d\t페어리: %-3d\t풀: %-3d\n",
				my_item->P_token[9], my_item->P_token[10], my_item->P_token[11]);

	printf("	----------------------------------------------\n");
	printf("	▶ Press Pokemon's number you want to see\n");
	printf("	▶ 0. Go to menu\n");
	printf("	----------------------------------------------\n");

	printf("\n");

	for (int i = 0; i < my_item->My_Pokemon[0].total; i++)
	{
		int level = my_item->My_Pokemon[i].level;
		
		

		char name[20];

		switch (level)
		{
		case 1:
			strcpy(name, my_item->My_Pokemon[i].name_1);
		case 2:
			strcpy(name, my_item->My_Pokemon[i].name_2);
		case 3:
			strcpy(name, my_item->My_Pokemon[i].name_3);
		case 4:
			strcpy(name, my_item->My_Pokemon[i].name_1); //전설급
		}

		if (level < 3)
		{
			printf("	%d) %s %s", i + 1, name, my_item->My_Pokemon[i].type);
			printf("	:: 진화 %d 단계\n\n", level);
		}
		else if (level >= 3)
		{
			printf("	%d) %s %s", i + 1, name, my_item->My_Pokemon[i].type);
			printf("	:: 진화 : 최종단계\n\n");
		}

	}

	int n;

	printf("	Press the key >> ");
	scanf("%d", &n);

	if (n == 0) Pokemon_Menu(my_money, my_item);

	if (n != 0) Show_pokemon(my_item, my_money, n);

}

void Show_pokemon(ITEM* my_item, WALLET* my_money, int index)
{
	index--;

	int level = my_item->My_Pokemon[index].level;
	char name[20];
	
	switch (level)
	{
	case 1:
		strcpy(name, my_item->My_Pokemon[index].name_1);
		break;
	case 2:
		strcpy(name, my_item->My_Pokemon[index].name_2);
		break;
	case 3:
		strcpy(name, my_item->My_Pokemon[index].name_3);
		break;
	case 4:
		strcpy(name, my_item->My_Pokemon[index].name_1);
		break;//전설급
	}

	if (level == 2 && strstr(my_item->My_Pokemon[index].name_3, "x"))
	{
		level++;
	}

	char type[20];
	strcpy(type, my_item->My_Pokemon[index].type);

	system("cls");

	printf("\n");
	printf("	My Pokemon Detail\n");
	printf("	==============================================\n");
	printf("	[%s]\n", name);
	printf("	◎Type : %s", type);

	switch (level)
	{
	case 1:
		printf("	★ %s로 진화할 수 있습니다!\n", my_item->My_Pokemon[index].name_2);
		break;

	case 2:
		printf("	★★ %s로 진화할 수 있습니다!\n", my_item->My_Pokemon[index].name_3);
		break;
	
	case 3:
		printf("	★★★ 최종진화 상태입니다!\n");
		break;

	case 4:
		printf("	★★★ 최종진화 상태입니다!\n");
		break;

	}

	printf("	==============================================\n");
	
	int n;
	printf("\n");
	printf("	※ 돌아가려면 0을 누르세요!\n");

	if (level < 3)
	{
		
		printf("	※ 진화 시키려면 1을 누르세요!\n");
		printf("\n");
		

	}
	
	printf("	Press the key >> ");

	scanf("%d", &n);
	if (n == 0) My_pokemon(my_item, my_money);

	if (n == 1)
	{
		if (my_item->P_token[my_item->My_Pokemon[index].type_num] > 0)
		{
			system("cls");
			printf("	\n\n	==============================================\n");
			printf("	★진화 성공★\n");

			switch (level)
			{
			case 1:
				my_item->My_Pokemon[index].level++;
				printf("	★[%s]가 -> [%s]로 진화하였습니다!\n", name, my_item->My_Pokemon[index].name_2);
			
				printf("	==============================================\n");

				printf("\n");
				printf("	Press any key >> ");

				int key = 0;
				scanf("%d", &key);
				My_pokemon(my_item, my_money);
				break;

			case 2:

				my_item->My_Pokemon[index].level++;
				printf("	★[%s]가 -> [%s]로 진화하였습니다!\n", name, my_item->My_Pokemon[index].name_3);

				printf("	==============================================\n");

				printf("\n");
				printf("	Press any key >> ");

				key = 0;
				scanf("%d", &key);
				My_pokemon(my_item, my_money);
				break;
			
			}
		}


		else if (my_item->P_token[my_item->My_Pokemon[index].type_num] == 0)
		{
			printf("	You don't have enough Token!\n");
			printf("	Press any key >> ");
			scanf("%d", &n);
			Show_pokemon(my_item, my_money, index);
		}

		int key;
		scanf("%d", &key);
		My_pokemon(my_item, my_money);

	}

}
