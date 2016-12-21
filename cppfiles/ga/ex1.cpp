/**************************************
ロボット知能学
GA　サンプルプログラム
**************************************/

#include<stdio.h>
#include<stdlib.h>
#include<time.h>

int calc_fitness(int individual, int length, int **population);
void roulette_selection(int num, int length, int **population, int *fitness);
void one_point_crossover(int crossover_rate, int mutation_rate, int num, int length, int **population, int **pair);
void pairing(int num, int length, int **population, int **pair);
void mutation(int mutation_rate, int length, int individual, int **population);
double average_fitness(int num, int *fitness);

int main()
{
    int **population;       //個体集合
    int **pair;             //個体集合を並べ換え，上から順にペアにしたもの
    int num;                //個体数
    int length;             //遺伝子長
    int *fitness;           //適応度
    int generation;         //世代
    int max_generation;     //進化を終了する世代
    int crossover_rate;     //交叉率[%]
    int mutation_rate;      //突然変異率[%]
    double gole;            //目標適応度

    int i, j;

    num = 10;
    length = 10;
    crossover_rate = 50;
    mutation_rate = 5;
    gole = 90;

    //個体集合
    population = new int *[num];
    for(i=0; i<num; i++){
        population[i] = new int[length];
    }
    pair = new int*[num];
    for(i=0; i<num; i++){
        pair[i] = new int[length];
    }

    //適応度
    fitness = new int[num];

    //乱数の初期化
    srand((unsigned)time(NULL));

    //初期個体の生成
    for(i=0; i<num; i++){
        for(j=0; j<length; j++){
            population[i][j] = rand()%2;
            printf("%d", population[i][j]);
        }
    }

    //結果の保存準備
    FILE *fp;
    fp = fopen("fitness.csv", "w");
    fclose(fp);
    
    //進化開始
    for(generation=0; generation<max_generation; generation++){
        printf("generation = %d\n", generation);
        
        //ペアリング
        pairing(num, length, population, pair);

        //交叉，突然変異
        one_point_crossover(crossover_rate, mutation_rate, num, length, population, pair);

        //適応度の計算
        for(i=0; i<num; i++){
            fitness[i] = calc_fitness(i, length, population);

            //確認
            for(j=0; j<length; j++){
                printf("%d", population[i][j]);
            }
            printf(" fitness = %d\n", fitness[i]);
        }

        //結果を保存
        FILE *fp;
        fp = fopen("fitness.csv", "a");
        fprintf(fp, "%d, %lf\n", generation, average_fitness(num, fitness));
        fclose(fp);

        //終了判定
        if(average_fitness(num, fitness) > gole){
            printf("目標適応度に到達したため終了します\n");
            break;
        }

        //ルーレット選択
        roulette_selection(num, length, population, fitness);
    }

    for(i=0; i<num; i++){
        delete[]population[i];
        delete[]pair[i];
    }
    delete[]population;
    delete[]pair;
    delete[]fitness;

    return 0;
}

int calc_fitness(int individual, int length, int **population)
{
    int i;
    int fitness = 0;
    
    for(i=0; i<length; i++){
        fitness = fitness + population[individual][i];
    }
    return 10 * fitness;
}

void roulette_selection(int num, int length, int **population, int *fitness)
{
    int i, j, k;
    int sum_fitness;
    int **new_population;           //選ばれた個体が入る
    double *roulette;                   //選択された確率が入る
    double *ac_roulette;            //rouletteの累積値が入る
    double r;                                   //ルーレットで使う乱数

    new_population = new int*[num];
    for(i=0; i<num; i++){
        new_population[i] = new int[length];
    }

    roulette = new double[num];
    ac_roulette = new double[num];

    //fitnessの和を求める
    sum_fitness = 0;
    for(i=0; i<num; i++){
        sum_fitness = sum_fitness + fitness[i];
    }

    //ルーレットを作る
    roulette[0] = (double)fitness[0] / (double)sum_fitness;
    ac_roulette[0] = roulette[0];

    for(i=0; i<num; i++){
        roulette[i] = (double)fitness[i] / (double)sum_fitness;
        ac_roulette[i] = ac_roulette[i-1] + roulette[i];
    }

    //ルーレットを使って選択する
    for(i=0; i<num; i++){
        r = (double)rand() / (double)RAND_MAX;
        for(j=0; j<num; j++){
            if(r <= ac_roulette[j]){
                for(k=0; k<length; k++){
                    new_population[i][k] = population[j][k];
                }
                break;
            }
        }
    }

    //new_populationをpopulationにコピー
    for(i=0; i<num; i++){
        for(k=0; k<length; k++){
            population[i][k] = new_population[i][k];
        }
    }
}

void one_point_crossover(int crossover_rate, int mutation_rate, int num, int length, int **population, int **pair)
{
    int i, j;
    int cross_point;

    for(i=0; i<(num-1); i=i+2){
        if(rand() % 100 < crossover_rate){
            //交叉実行
            cross_point = rand() % (length - 1) + 1;
            //printf("cross_point=%d \n", cross_point);
            for(j=0; j<cross_point; j++){
                population[i][j] = pair[i+1][j];
                population[i+1][j] = pair[i][j];
            }
            for(j=cross_point; j<length; j++){
                population[i][j] = pair[i][j];
                population[i+1][j] = pair[i+1][j];
            }

            //突然変異実行
            mutation(mutation_rate, length, i, population);
            mutation(mutation_rate, length, i+1, population);
        }else{
            //交叉を行わず，そのままpairをpopulationにコピー
            for(j=0; j<length; j++){
                population[i][j] = pair[i][j];
                population[i+1][j] = pair[i+1][j];
            }
        }
    }
}

void mutation(int mutation_rate, int length, int individual, int **population)
{
    int i;
    
    for(i=0; i<length; i++){
        if(mutation_rate > rand() % 100){
            population[individual][i] =! population[individual][i];
        }
    }
}

void pairing(int num, int length, int **population, int **pair)
{
    int *shuffle;               //個体番号を入れ，シャッフルするための配列
    int r;                          //乱数
    int i, j;
    int temp;

    shuffle = new int[num];

    //初期化
    for(i=0; i<num; i++){
        shuffle[i] = i;
    }

    //シャッフル
    for(i=0; i<num; i++){
        r = rand() % num;
        temp = shuffle[r];
        shuffle[r] = shuffle[i];
        shuffle[i] = temp;
    }

    //shuffleの確認
    //for(i=0; i<num; i++){
    //  printf("shuffle[%d]=%d\n", i, shuffle[i]);
    //}

    //populationからペアを作りpairにコピー
    for(i=0; i<num; i++){
        for(j=0; j<length; j++){
            pair[i][j] = population[shuffle[i]][j];
        }
    }

    //確認
    /*for(i=0; i<num; i++){
            for(j=0; j<length; j++){
                printf("%d", population[i][j]);
            }
            printf(">>>");
            for(j=0; j<length; j++){
                printf("%d", pair[i][j]);
            }
            printf("\n");
        }
    */
}

double average_fitness(int num, int *fitness)
{
    int i;
    int sum = 0;

    for(i=0; i<num; i++){
        sum = sum + fitness[i];
    }
    
    return (double)sum / (double)num;
}














