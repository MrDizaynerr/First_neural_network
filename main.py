import neuron as n
import PySimpleGUI as ps
import re

inp_dat = input('Enter data: ').split()
inp_dat = [int(x) for x in inp_dat]
learn_speed = 0.5

layout = [[ps.Text('Learn speed', size=(20, 1)), ps.Input()],
          [ps.Text('Enter data here', size=(20, 1)), ps.Input()],
          [ps.Text('Enter right here', size=(20, 1)), ps.Input()],
          [ps.Text('Output', size=(20, 1)), ps.Text('OUT_HERE', key='out', size=(80, 1))],
          [ps.Text('Error:', size=(20, 1)), ps.Text('ERROR_HERE', key='err', size=(80, 1))],
          [ps.Button('Proceed'), ps.Button('Exit')]]

window = ps.Window('AI Learn', layout)

web = []
web.append([n.Neuron(inp_dat) for _ in range(2)])
web.append([n.Neuron(web[0]) for _ in range(3)])
web.append([n.Neuron(web[1]) for _ in range(3)])
web.append([n.Neuron(web[2]) for _ in range(3)])
web.append([n.Neuron(web[3]) for _ in range(3)])
web.append([n.Neuron(web[4])])

print('web created')

right_ans = 1


def learn(right_ans):
    got_ans = web[-1][-1].output()
    err = right_ans - got_ans
    #print('answer is:', got_ans)
    #print('error is:', err)
    web[-1][-1].my_err = err

    for i in range(len(web[len(web) - 1])):
        web[len(web) - 1][i].my_err = err
    for i in range(len(web) - 2, 0, -1):
        for j in range(len(web[i + 1])):
            for k in range(len(web[i])):
                web[i][k].my_err += web[i + 1][j].my_err * web[i + 1][j].weights[k]
    for i in range(len(web)):
        for j in range(len(web[i])):
            for k in range(len(web[i][j].weights)):
                web[i][j].weights[k] = web[i][j].weights[k] + web[i][j].my_err * web[i][j].dsygm() * learn_speed
    for i in range(len(web) - 2, 0, -1):
        for j in range(len(web[i + 1])):
            for k in range(len(web[i])):
                web[i][k].my_err = 0

    for i in range(len(web)):
        for j in range(len(web[i])):
            with open('wgt' + str(i) + str(j), 'w') as wr:
                for x in web[i][j].weights:
                    wr.write(str(x))
                    wr.write(' ')
    return got_ans


def proceed(inp_vals):
    try:
        for i in range(len(web[0])):
            web[0][i].set_dat(inp_vals)
        return web[-1][0].output()
    except:
        print('Error input data')
        return None

'''
learning_proc = True
while learning_proc:
    inp_dat = input('Enter data: ').split()
    inp_dat = [int(x) for x in inp_dat]
    proceed(inp_dat)
    must_be = int(input('Enter right answer: '))
    learn(must_be)
    learning_proc = True if input('Continue? y/n ') == 'y' else False'''

while True:
    act, dat = window.read()
    if act == 'Proceed':
        if ',' in dat[0]:
            learn_speed = float('.'.join(dat[0].split(',')))
        else:
            learn_speed = float(dat[0])
        if '' in dat:
            ps.Popup('Must enter data with answer')
        else:
            inp_dat = dat[1].split()
            inp_dat = [float(x) for x in inp_dat]
            proceed(inp_dat)
            must_be = float(dat[2])
            got_ans = learn(must_be)
            window.FindElement('out').Update(learn(must_be))
            window.FindElement('err').Update(must_be-got_ans)
    if act == 'Exit':
        break