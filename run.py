import gaurabda as gcal

loc = gcal.GCLocation(data = {
    'latitude': 27.583,
    'longitude': 77.73,
    'tzname': '+5:30 Asia/Calcutta',
    'name': 'Vrindavan, India'
})

d = gcal.GCGregorianDate(date=gcal.Today(), day=1)


tc = gcal.TCalendar()
tc.CalculateCalendar(loc,d,65)

# save results in various formats
#with open('calendar.txt','wt') as wf:
#    tc.write(wf, format='plain')
#with open('test/calendar.rtf','wt') as wf:
#    tc.write(wf, format='rtf')
#with open('test/calendar.html','wt') as wf:
#    tc.write(wf)
#with open('test/calendar2.html','wt') as wf:
#    tc.write(wf, layout='table')
with open('calendar.json','wt') as wf:
    tc.write(wf, format='json')