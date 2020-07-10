import csv
import numpy as np
import operator
import random
import copy
global prerequisite_array
global array
global Temp_individual

ps=200
mg=100
ts=20
sw=3
sh=15
af=15
is_initial=30

n_courses=66
n_periods=12
load_per_period_lb=10
load_per_period_ub=20
courses_per_period_lb=2
courses_per_period_ub=10



Temp_individual=[[]for i in range(n_periods)]

courses = ["dew100","fis100","hcw310","iwg101","mat111","mat121","dew101","fis110","iwi131","mat112","mat122","dewxx0","fis120","hcw311","hxwxx1","ili142","mat113","mat123","fis130","ili134","ili151","iwm185","mat124","fis140","hxwxx2","ile260","ili260","iwn170","qui104","ili231","ili243","ili252","ili273","mat210","mat260","ild208","ili221","ili274","ili281","iwn270","mat270","hrw150","ili238","ili242","ili275","ili355","hrw110","ici393","ili237","ili334","ili363","iwn261","hrw100","ici382","ili331","ili362","ili381","iln230","ici313","ici315","ici332","ici344","icn336","iwi365","ici314","ici367"];
course_load = [1, 3, 1, 2, 4, 4, 1, 5, 3, 4, 4, 1, 4, 1, 1, 4, 4, 4, 4, 4, 3, 3, 4, 4, 1, 3, 3, 3, 3, 3, 4, 4, 3, 4, 4, 3, 4, 3, 3, 3, 4, 2, 4, 3, 3, 4, 2, 4, 4, 4, 3, 3, 2, 4, 4, 3, 3, 3, 2, 2, 3, 4, 3, 3, 2, 2 ];
#print(len(course_load))
total_credits=0
for t in range(n_courses):
 total_credits=total_credits+course_load[t]
mean_credits= total_credits / n_periods
temp_array={}
for t in range(n_courses):
	temp_array[t]=0
prerequisite_array=[ [] for i in range(n_courses)]
prerequisite_array_inverse=[[] for i in range(n_courses)]

array=prerequisite_array.copy()

def search(p):
	for i in range(n_courses):
		if(courses[i]==p):
			return i
def prerequisite(prereq):
	for i in range(len(prereq)):
		t1=search(prereq[i][0])
		t2=search(prereq[i][1])
		prerequisite_array[t1].insert(0,t2)
		prerequisite_array_inverse[t2].insert(0,t1)
	#print(prerequisite_array)

def func(prerequisite_array,temp_array):
	array=prerequisite_array.copy()
	for i in range(n_courses):
		j=0
		while(j<len(array[i])):
			k=array[i][j]
			for l in range(len(array[k])):
				if array[k][l] not in array[i]:
					array[i].append(array[k][l])
			j+=1
	return array

def check_course_constraints(p,c,Temp_individual):
	sum=0
	flag1=0
	flag2=0
	for i in Temp_individual[p]:
		sum+=course_load[i]
	sum+=course_load[c]
	if(sum>load_per_period_ub):
		flag1=0
	else:
		flag1=1
	if(len(Temp_individual[p])>=courses_per_period_ub):
		flag2=0
	else:
		flag2=1
	flag=flag1 and flag2
	return flag

def isrcbefore(p,c,Temp_individual):
	rc=prerequisite_array[c]
	flag=1
	if(len(rc)>=1 and p==0):
		return 0
	for i in rc:
		for j in range(p):
			if i in Temp_individual[j]:
				flag=1
				break
			else:
				flag=0
		if(flag==0):
			return 0
	return 1

def isrcafter(p,c,Temp_individual):
	rci=prerequisite_array_inverse[c]
	flag=1
	if(len(rci)>=1 and p==(n_periods-1)):
		return 0
	for i in rci:
		for j in range(p+1,n_periods):
			if i in Temp_individual[j]:
				flag=1
				break
			else:
				flag=0
		if(flag==0):
			return 0
	return 1

	

def can_course_settle(p,c,Temp_individual):
	flag=1

	for i in range(p+1):
		if c in Temp_individual[i] :
			flag=0
			break
	return (flag )

def count_prerequisite(array):
	for i in range(n_courses):
		temp_array[i]=len(array[i])

def min_credit(p,c_removed,Temp_individual):
	sum=0
	for i in range(len(Temp_individual[p])):
		sum+=course_load[Temp_individual[p][i]]
	sum1=sum-course_load[c_removed]
	if(sum1>load_per_period_lb):
		return 1
	else:
		return 0

def min_credit_constraints(p,c_added,c_removed,Temp_individual):
	sum=0
	for i in range(len(Temp_individual[p])):
		sum+=course_load[Temp_individual[p][i]]
	sum1=sum+course_load[c_added]-course_load[c_removed]
	if(sum1>load_per_period_lb ):
		return 1
	else:
		return 0

def credit_constraints(p,c_added,c_removed,Temp_individual):
	sum=0
	for i in range(len(Temp_individual[p])):
		sum+=course_load[Temp_individual[p][i]]
	sum1=sum+course_load[c_added]-course_load[c_removed]
	if(sum1>=load_per_period_lb and sum1<=load_per_period_ub):
		return 1
	else:
		return 0

def swap(p,q,Temp_individual):
	
	while(1):
		p1=random.randint(0,len(Temp_individual[p])-1)
		CL_p=Temp_individual[p][p1]
		p2=random.randint(0,len(Temp_individual[q])-1)
		CL_q=Temp_individual[q][p2]
		t1=0
		#print(CL_p,CL_q,"   c")

		if(p<q):
			t1=p
			t2=q
			c1=CL_q
			c2=CL_p
		else:
			t1=q
			t2=p
			c1=CL_p
			c2=CL_q

		

		if(not(credit_constraints(p,CL_q,CL_p,Temp_individual) and credit_constraints(q,CL_p,CL_q,Temp_individual))):
			return 0
		else:
			if(not(isrcbefore(t1,c1,Temp_individual) and isrcafter(t2,c2,Temp_individual))):
				
				return 0
			else:
				Temp_individual[p].remove(CL_p)
				Temp_individual[p].append(CL_q)
				Temp_individual[q].remove(CL_q)
				Temp_individual[q].append(CL_p)		
				return 1						

def best_solution(Individual): #Find out thr best chromosome from the population i.e chromosome having the least maximum load per period
	dic={}
	
	for i in range(len(Individual)):
		minimum=0
		temp=Individual[i]
		calc=0
		for j in range(len(temp)):
			temp1=temp[j]
			sum1=0
			for k in range(len(temp1)):
				sum1+=course_load[temp1[k]]
			if(sum1>minimum):
				minimum=sum1
			calc+=(abs(sum1-mean_credits)/mean_credits)
		dic[i]=1/(1+calc)
	best_popn=min(dic.items(),key=lambda x:x[1])[0]
	best=min(dic.items(),key=lambda x:x[1])[1]
	worst=max(dic.items(),key=lambda x:x[1])[1]
	#print(best,worst)
	return (best_popn)

def better_solution(sc,sb,Individual): #To find better solution between two solutions
	
	min_c=min_b=0
	temp_c=Individual[sc]
	temp_b=Individual[sb]
	calc=0

	for j in range(len(temp_c)):
		temp1=temp_c[j]
		sum1=0
		for k in range(len(temp1)):
			sum1+=course_load[temp1[k]]
		calc+=(abs(sum1-mean_credits)/mean_credits)
		min_c=1/(1+calc)
	for j in range(len(temp_b)):
		temp1=temp_b[j]
		sum1=0
		for k in range(len(temp1)):
			sum1+=course_load[temp1[k]]
		calc+=(abs(sum1-mean_credits)/mean_credits)
		min_b=1/(1+calc)	
	if(min_c<min_b):
		return 1
	return 0

def max_credits(sb,Individual):
	min_b=0
	temp_b=Individual[sb]
	for j in range(len(temp_b)):
		temp1=temp_b[j]
		sum1=0
		for k in range(len(temp1)):
			sum1+=course_load[temp1[k]]
		if(sum1>min_b):
			min_b=sum1

	return(min_b)


def mutate_swap(I,sw):
	Im=copy.deepcopy(I)
	i=0
	while(i<=sw):
		flag=0
		while(flag!=1):

			p=random.randint(0,n_periods-1)
			q=random.randint(0,n_periods-1)
			while(p==q):
				q=random.randint(0,n_periods-1)

			p1=random.randint(0,len(Im[p])-1)
			CL_p=Im[p][p1]
			p2=random.randint(0,len(Im[q])-1)
			CL_q=Im[q][p2]
			t1=t2=0
			

			if(p<q):
				t1=p
				t2=q
				c1=CL_q
				c2=CL_p
			else:
				t1=q
				t2=p
				c1=CL_p
				c2=CL_q

			#print(p,q)

			if(not(credit_constraints(p,CL_q,CL_p,Im) and credit_constraints(q,CL_p,CL_q,Im))):
				flag=0
				#print("flag0")
			else:
				if(not(isrcbefore(t1,c1,Im) and isrcafter(t2,c2,Im))):
					flag=0
					#print("flag1")
				else:
					Im[p].remove(CL_p)
					Im[p].append(CL_q)
					Im[q].remove(CL_q)
					Im[q].append(CL_p)		
					flag=1
					#print("flag")
		i=i+1						
	return Im
def check_constraints_shift(p_added,p_removed,c,Im):
	sum1=0
	for i in range(len(Im[p_added])):
		sum1+=course_load[Im[p_added][i]]
	sum1=sum1+course_load[c]
	sum2=0
	for i in range(len(Im[p_removed])):
		sum2+=course_load[Im[p_removed][i]]
	sum2=sum2-course_load[c]
	if(len(Im[p_added])>=courses_per_period_ub):
		return 0
	if (len(Im[p_removed])<=courses_per_period_lb):
		return 0
	if(sum1>load_per_period_ub):
		return 0
	if(sum2<load_per_period_lb):
		return 0
	return 1

def mutate_shift(I,sh):
	Im=copy.deepcopy(I)
	i=1
	while(i<=sh):
		flag=0
		while(flag==0):
			p=random.randint(0,n_periods-1)
			p1=random.randint(0,len(Im[p])-1)
			while(not(min_credit(p,p1,Im))):
				p=random.randint(0,n_periods-1)
				p1=random.randint(0,len(Im[p])-1)
			c1=Im[p][p1]

			q=random.randint(0,n_periods-1)
			while(p==q):
				q=random.randint(0,n_periods-1)
			#print(p,q,p1,c1)
			if(check_constraints_shift(q,p,c1,Im)):
				#print("q")
				if(p>q):
					if(isrcbefore(q,c1,Im)):
						Im[p].remove(c1)
						Im[q].append(c1)
						flag=1
					else:
						flag=0
				else:
					if(isrcafter(q,c1,Im)):
						Im[p].remove(c1)
						Im[q].append(c1)
						flag=1
					else:
						flag=0
		i=i+1
	return Im

def select_individual(Individual,ts):
	i=0
	p=random.randint(0,len(Individual)-1)
	while i<ts:
		q=random.randint(0,len(Individual)-1)
		#print(p,q)
		if(not(better_solution(p,q,Individual))):
			p=q
		i=i+1
	#print("^")
	return Individual[p]

def fitness_func(Individual):  #Find out the fitness of the population 
	dic={}
	for i in range(len(Individual)):
		temp=Individual[i]
		calc=0
		for j in range(len(temp)):
			temp1=temp[j]
			sum1=0
			for k in range(len(temp1)):
				sum1+=course_load[temp1[k]]
			calc+=(abs(sum1-mean_credits)/mean_credits)
		dic[i]=1/(1+calc)
	#print(dic)
	#print()
	#best_popn=min(dic.items(),key=lambda x:x[1])[0]
	best=min(dic.items(),key=lambda x:x[1])[1]
	worst=max(dic.items(),key=lambda x:x[1])[1]
	#print(best,worst)
	col2_array.append(best)
	col3_array.append(worst)
		
	return (dic)
    
def main():
	
	prereq =[            
	["dew101", "dew100"],
	["fis110", "fis100"],
	["fis110", "mat121"],
	["mat112", "mat111"],
	["mat122", "mat111"],
	["mat122", "mat121"],
	["dewxx0", "dew101"],
	["fis120", "fis110"],
	["fis120", "mat122"],
	["hcw311", "hcw310"],
	["ili142", "iwi131"],
	["mat113", "mat112"],
	["mat113", "mat122"],
	["mat123", "mat112"],
	["mat123", "mat122"],
	["fis130", "fis110"],
	["fis130", "mat122"],
	["ili134", "iwi131"],
	["ili151", "mat112"],
	["mat124", "mat113"],
	["mat124", "mat123"],
	["fis140", "fis120"],
	["fis140", "fis130"],
	["ile260", "fis120"],
	["ile260", "mat124"],
	["ili231", "iwi131"],
	["ili252", "iwi131"],
	["ili273", "ili260"],
	["mat210", "mat113"],
	["mat260", "iwi131"],
	["mat260", "mat113"],
	["mat260", "mat123"],
	["ili221", "ili134"],
	["ili221", "ili231"],
	["ili221", "mat260"],
	["ili274", "ili273"],
	["ili281", "mat260"],
	["mat270", "iwi131"],
	["mat270", "mat113"],
	["mat270", "mat123"],
	["ili238", "ili134"],
	["ili242", "ili142"],
	["ili275", "ili274"],
	["ili355", "ili221"],
	["hrw110", "hrw150"],
	["ici393", "mat210"],
	["ici393", "mat260"],
	["ili237", "ili231"],
	["ili237", "ili252"],
	["ili334", "ili238"],
	["ili363", "ili273"],
	["hrw100", "hrw110"],
	["ici382", "ili334"],
	["ili331", "ili238"],
	["ili331", "ili274"],
	["ili362", "ili363"],
	["ili381", "ili281"],
	["ili381", "mat210"],
	["iln230", "iwn170"],
	["ici313", "ili331"],
	["ici332", "ici393"],
	["ici332", "ili331"],
	["ici344", "ili243"],
	["icn336", "ici393"],
	["ici314", "ici313"]
   ];
	random.shuffle(prereq)
	prerequisite(prereq)
	
	l=0
	if(n_courses%n_periods==0):
		l=n_courses/n_periods
	else:
		l=int(n_courses/n_periods)+1
	
	array=func(prerequisite_array,temp_array)
	
	count_prerequisite(array)
	
	sorted_dict=sorted(temp_array.items(), key=operator.itemgetter(1))	
	var=0
	zero_prereq=[]
	for i in range(len(sorted_dict)):
		if(len(prerequisite_array_inverse[sorted_dict[i][0]])==0 and len(prerequisite_array[sorted_dict[i][0]])==0):
			zero_prereq.append(sorted_dict[i][0])
	
	while(var<10):
		c=0
		sp=0
	
		while(c<n_courses):
			
			k=sorted_dict[c][0]
			if k not in zero_prereq :
				RC=prerequisite_array[k]
				p=sp
		
				while(p<n_periods and can_course_settle(p,k,Temp_individual)):
		
					if(len(Temp_individual[p])<l):
		
						if (check_course_constraints(p,k,Temp_individual) and isrcbefore(p,k,Temp_individual)):
							Temp_individual[p].append(k)
		
					else:
						sp+=1
					p+=1
			c+=1
		var+=1
	for i in zero_prereq:
		for j in range(n_periods):
			if(len(Temp_individual[j])==0):
				Temp_individual[j].append(i)
				zero_prereq.remove(i)
				break
	
	for i in range(len(zero_prereq)):
		for j in range(n_periods):
			if(len(Temp_individual[j])<l):
				Temp_individual[j].append(zero_prereq[i])
				break

	j=0
	Individual=[[] for i in range(ps)]
	while(j<ps):
		i=0
		k=0
		while(i<is_initial or k<5 ):
			p=random.randint(0,n_periods-1)
			q=random.randint(0,n_periods-1)
			while(p==q):
				q=random.randint(0,n_periods-1)
			k+=swap(p,q,Temp_individual)
			i+=1
		Individual[j]=copy.deepcopy(Temp_individual)
		j+=1

	#for i in range(len(Individual)):
		#print("Individual",i,"= ",Individual[i])
	
	sb=best_solution(Individual)
	k=1
	j=1
	
	while (j<=mg):
		sc=best_solution(Individual)
	
		if(better_solution(sc,sb,Individual)):
			sb=copy.deepcopy(sc)
		q=[[] for i in range(ps)]
		i=0
		#print("2")
		while(i<ps):
			#print("4")
			I=select_individual(Individual,ts)
			#print("I")
			#print(I)
			if k<1:
				#print("8")
				Im=mutate_swap(I,sw)
				q[i]=copy.deepcopy(Im)
				#print("81")
			else:
				#print("16")
				Im=mutate_shift(I,sh)
				q[i]=copy.deepcopy(Im)
				#print("61")
			#print(q[i])
			i=i+1
		#print("1")
		Individual=copy.deepcopy(q)
		k=(int(j/af))%2
		j=j+1

	optimal_solution=max_credits(sb,Individual)
	k=best_solution(Individual)
	print("Curriculum:")
	for i in range(len(Individual[sb])):
		print('Period ',i+1,': ',end=" ")
		for j in range(len(Individual[sb][i])):
			print(courses[Individual[sb][i][j]],end=" ")
		print()


	print("optimal solution:",optimal_solution)
	

if __name__ == '__main__':
	main()