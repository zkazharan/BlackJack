import algo
import dataTemp
import dataBase
import datetime

def logReg(): 
  algo.clear('all')
  algo.title('UKT BLACKJACK', 50)

  print(' [1] Login')
  print(' [2] Register')
  print(' [3] Exit')

  algo.border(50)

  menu = input(' Choose Menu: ')
  
  if menu == '1':
    login()
    return
  elif menu == '2':
    register()
    return
  elif menu == '3':
    algo.loading('Exiting program', 3)
    return
  else:
    algo.notif('Wrong menu input !', 50, 1)
    logReg()
    return
  return

def login():
  algo.clear('all')
  algo.title('UKT BLACKJACK', 50)
  print("Input '#' for cancel")
  username = input(' Username: ')

  if username == "":
    algo.notif("Username can't be empty !", 50, 1)
    login()
    return
  elif username == "#":
    logReg()
    return
  
  if dataBase.isUsernameExist(username) == False:
    algo.notif('Username not found !', 50, 1)
    login()
    return
  
  password = input(' Password: ')
  if password == "":
    algo.notif("Username can't be empty !", 50, 1)
    register()
    return
  elif password == "#":
    logReg()
    return
  
  if password != dataBase.getPassword(username):
    algo.notif('Wrong Password !', 50, 1)
    login()
    return
  dataTemp.account = username

  main()

def register():
  algo.clear('all')
  algo.title('UKT BLACKJACK', 50)
  print("Input '#' for cancel")
  username = input(' New Username: ')

  if username == "":
    algo.notif("Username can't be empty !", 50, 1)
    register()
    return
  elif username == "#":
    logReg()
    return
  elif dataBase.isUsernameExist(username) == True:
    algo.notif('Username is already exist !', 50, 1)
    register()
    return
  
  password = input(' Password: ')
  if password == "":
    algo.notif("Username can't be empty !", 50, 1)
    register()
    return
  elif password == "#":
    logReg()
    return

  dataBase.addUser(username, password)
  algo.notif("Register Success!", 50, 1)
  logReg()

def main() :
  dataBase.addLogin(dataTemp.account)
  algo.clear('all')
  
  algo.title('UKT BLACKJACK', 50)
  print(' [1] Play')
  print(' [2] Claim Rewards')
  print(' [3] My Profile')
  print(' [4] Leaderboard')
  print(' [5] Logout')
  algo.border(50)

  menu = input(' Choose Menu: ')

  if menu == '1':
    betMenu()
    return
  elif menu == '2':
    claim()
    main()
    return
  elif menu == '3':
    myProfile()
    return
  elif menu == '4':
    leaderBoard()
    return
  elif menu == '5':
    logReg()
    return
  else:
    algo.notif('Wrong menu input !', 50, 1)
    main()

def betMenu():
  algo.clear('all')
  
  algo.title('UKT BLACKJACK', 50)
  print("Type '#' for cancel")
  menu = input(' How much you want to bet?: ')

  if menu == "":
    algo.notif("Bet value can't be empty !", 50, 1)
    betMenu()
    return
  if menu == "#":
    main()
    return
  
  try:
    bet = int(menu)
  except:
    algo.notif('Bet value must be a integer !', 50, 1)
    betMenu()
    return
  
  if bet < 1000:
    algo.notif('Minimum bet is 1000 !', 50, 1)
    betMenu()
    return
  
  if bet > dataBase.getChip(dataTemp.account):
    algo.notif("You don't have enough chip !", 50, 1)
    betMenu()
    return

  dataBase.setChip(dataTemp.account, -(bet))
  
  dataTemp.bet = bet
  play()
  return

def claim():
  if(dataBase.getClaimDate(dataTemp.account) == 0):
    algo.notif('You earned ⍟ 1250', 50, 2)
    dataBase.setChip(dataTemp.account, 1250)
    dataBase.addClaimDate(dataTemp.account)
    return
  elif((dataBase.getLastLogin(dataTemp.account) - dataBase.getClaimDate(dataTemp.account)).total_seconds() > 86400):
    algo.notif('You earned ⍟ 1250', 50, 2)
    dataBase.setChip(dataTemp.account, 1250)
    dataBase.addClaimDate(dataTemp.account)
    return
  else:
    secToDay = (dataBase.getLastLogin("Asada") - dataBase.getClaimDate("Asada")).total_seconds()
    algo.notif("You can claim after " + str(datetime.timedelta(seconds=secToDay)), 50, 3)
    return

def myProfile():
  chips = dataBase.getChip(dataTemp.account)
  totalMatch = dataBase.getMatches(dataTemp.account)
  totalWin = dataBase.getWins(dataTemp.account)
  totalLose = dataBase.getLoses(dataTemp.account)
  algo.clear('all')
  
  algo.title('UKT BLACKJACK', 50)

  print("Your Profile")
  print(" Username: " + dataTemp.account)
  print(" Chips: ⍟ " + str(chips))
  print(" Matches: " + str(totalMatch))
  print(" Win: " + str(totalWin))
  print(" Lose: " + str(totalLose))
  try:
    winrate = (totalWin / totalMatch) * 100
    print(" Win Rate: " + str(round(winrate, 1)) + "%")
  except:
    print(" Win Rate: 0%")

  menu = input("Type '#' for back\n")

  if(menu == "#"):
    main()
    return
  else:
    myProfile()
    return

def leaderBoard():
  db = dataBase.dbUsers.find().sort("chip", -1)
  count = 1
  lb = ""
  for i in db:
    lb += " [" + str(count) + "] " + i["username"] + ": ⍟ " + str(i["chip"]) + "\n"
    count += 1
  
  algo.clear('all')
  
  algo.title('UKT BLACKJACK', 50)
  print("Leaderboard:\n" + lb)
  menu = input("Type '#' for back\n")

  if(menu == "#"):
    main()
    return
  else:
    leaderBoard()
    return

def play():
  dataBase.addMatch(dataTemp.account)
  algo.clear('all')

  if dataTemp.resetAll == True:
    algo.reset()
 
  if dataTemp.pCond == True:
    algo.giveCard(2, dataTemp.pCard, dataTemp.pValue)
    algo.giveCard(2, dataTemp.dCard, dataTemp.dValue)

  algo.calculate()

  algo.title('UKT BLACKJACK', 50)
  print("Bet: " + str(dataTemp.bet))
  print(' [»] Dealer\'s hand : ', end = '')
  algo.printFirstCard(dataTemp.dCard)

  print(' [»] Your hand     : ', end = '')
  algo.printCard(dataTemp.pCard)
  print('     Total         : ', dataTemp.pTotal)

  algo.border(50)
  algo.printMenu()
  algo.border(50)

  if dataTemp.pTotal >= 21:
    printResult()
    return

  while True:
    menu = input(' Your choice: ').upper()

    if menu == 'HIT':
      algo.giveCard(1, dataTemp.pCard, dataTemp.pValue)

      dataTemp.pCond = False
      dataTemp.resetAll = False

      play()
      return
    elif menu == 'STAND':
      stand()
      return
    else:
      algo.notif('Wrong menu Input !', 50, 1)
      algo.clear(3)

def stand():
  algo.clear('all')

  algo.calculate()

  algo.title('UKT BLACKJACK', 50)
  algo.printAll()
  algo.border(50)

  if dataTemp.dTotal < dataTemp.pTotal:
    algo.giveCard(1, dataTemp.dCard, dataTemp.dValue)
    algo.wait(1)
    algo.notif('Dealer Hit !', 50, 2)

    if dataTemp.dTotal > 21:
      printResult()
      return
    
    stand()
    return
  elif dataTemp.dTotal < 17 and dataTemp.dTotal == dataTemp.pTotal:
    algo.giveCard(1, dataTemp.dCard, dataTemp.dValue)
    algo.notif('Dealer Hit !', 50, 3)

    stand()
    return
  else:
    printResult()
    return

def printResult():
  algo.clear('all')

  algo.calculate()

  algo.title('UKT BLACKJACK', 50)
  algo.printAll()
  algo.border(50)

  if dataTemp.pTotal == dataTemp.dTotal:
    algo.result('Tie')
  elif dataTemp.pTotal == 21:
    algo.result('Blackjack')
  elif dataTemp.pTotal > 21:
    algo.result('pBusted')
  elif dataTemp.dTotal > 21:
    algo.result('dBusted')
  elif dataTemp.pTotal > dataTemp.dTotal:
    algo.result('Win')
  elif dataTemp.pTotal < dataTemp.dTotal:
    algo.result('Lose')

  algo.border(50)

  while True:
    again = input(' Play again (y/n) ? ').upper()
    if again == 'Y':
      dataTemp.resetAll = True
      betMenu()
      return
    elif again == 'N':
      dataTemp.resetAll = True
      main()
      return
    else:
      algo.notif('Wrong menu Input !', 50, 1)
      algo.clear(3)

logReg()