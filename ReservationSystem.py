from datetime import datetime
import time
import collections

class Reservation:
	def __init__(self, name, dateTime, partySize):
		self.name = name
		self.dateTime = dateTime
		self.partySize = partySize
		
	def __str__(self):
		return '%s with partySize %d at %s' % (self.name, self.partySize, self.dateTime)
	
	def __repr__(self):
		return str(self) 

class Scheduler:
	pass

# assumption is that each sitting in dining takes 1 hour
class TimeIntervalScheduler(Scheduler):
	
	def __init__(self, tableSize, nTables):
		self.tableSize = tableSize
		self.nTables = nTables
		self.timeSlot = 24
		self.scheduleMatrix = [[None for x in range(self.nTables)] for x in range(self.timeSlot)]
		
	def __str__(self):
		reservationSet = set()
		for i in range(len(self.scheduleMatrix)):
			for j in range(len(self.scheduleMatrix[i])):
				
				reservation = self.scheduleMatrix[i][j] 
				if reservation != None and reservation not in reservationSet:
					reservationSet.add(reservation)
			
		ret = ''
		for reservation in reservationSet:
			ret += str(reservation)
		return ret
		
	def MakeReservation(self, reservation):
		time = reservation.dateTime.time()
		
		# take the ceiling
		neededTableCount = reservation.partySize / self.tableSize + 1
		
		availableTableCount = 0
		availableTable = []
		for i in range(self.nTables):
			if self.scheduleMatrix[time.hour][i] == None:
				availableTableCount += 1
				availableTable.append(i)
		
		if availableTableCount < neededTableCount:
			return False
		
		for i in range(neededTableCount):
			col = availableTable[i]
			
			# the spot is taken
			self.scheduleMatrix[time.hour][col] = reservation
			
			if time.minute != 0 and time.hour <= self.timeSlot - 1:
				self.scheduleMatrix[time.hour + 1][col] = reservation
						
		return True
				
class Restaurant:
	
	def __init__(self, scheduler, tableSize=4, nTables=10):
		self.tableSize = tableSize
		self.nTables = nTables	
		self.reservationDateDict = collections.defaultdict(lambda:scheduler(self.tableSize, self.nTables))
		self.reservationNameDict = collections.defaultdict(lambda:[])
		
	def MakeReservation(self, reservation):
		
		date = reservation.dateTime.date()
		dailySchedule = self.reservationDateDict[date]
		
		# successfully made reservation
		if dailySchedule.MakeReservation(reservation):
			self.reservationNameDict[reservation.name].append(reservation)
			print 'Reservation made at %s' % reservation.dateTime
		else:
			print 'Reservation is not available at this time: %s' % reservation.dateTime
			
	def LookUpReservationByName(self, name):
		if self.reservationNameDict.get(name):
			print self.reservationNameDict.get(name)
		else:
			print 'There is no reservation under this name %s' % name
			
	def LookUpReservationByDate(self, date):
		if isinstance(date, datetime):
			date = date.date()
			
		if self.reservationDateDict.get(date):
			print self.reservationDateDict.get(date)
		else:
			print 'There is no schedule for this date %s' % date
					
def main():
	
	tableSize = 4
	nTables = 3
	# timeIntervalScheduler = TimeIntervalScheduler()
	restaurant = Restaurant(TimeIntervalScheduler, tableSize, nTables)
	
	name = 'cong hui'
	partySize = 4
	time = datetime.now()
	
	restaurant.MakeReservation(Reservation(name, time, partySize))
	
	name = 'cong hui'
	partySize = 3
	time = datetime(2015, 8, 8, 13, 30)
	
	restaurant.MakeReservation(Reservation(name, time, partySize))
	
	# restaurant.LookUpReservationByDate(time)
	

if __name__ == '__main__':
	main()
