#Test des fonctions xlwd

from xlwt import Workbook

test = Workbook()
feuille1=test.add_sheet('Feuille 1')

#Creation d'un curseur d'écriture en colomne (compteur)
cur_col=0
cur_row=0

row1=feuille1.row(cur_row)
hello="hello"
row1.write(cur_col,hello)
cur_col+=1
row1.write(cur_col,hello)
cur_row+=1
row1=feuille1.row(cur_row)
row1.write(cur_col,"zout")


test.save('test.xls')
