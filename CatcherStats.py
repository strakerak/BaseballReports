import numpy as np
import pandas as pd
from collections import defaultdict
from fpdf import FPDF
import math
import sys
import os
#DEBUG SETTINGS

shapedict = {'0':"Circle",'1':"Square",'2':"Diamond",'3':"TriangleUp",'4':"TriangleDown",'5':"PentagonUp",'6':"Hexagon",'7':"TriangleLeft",'8':"TriangleRight",'9':"PentagonDown",'10':"ThreeStar",'11':"FourStar",'12':"FiveStar",'13':"SixStar"}

def create_table_statline(table_data,topline,pdf,title='',data_size=10,title_size=12,align_data='C',cell_width='even',x_start='C',emphasize_data=[],emphasize_style=None,emphasize_color=(0,0,0)):
    #print(table_data[0])
    header = table_data[0]
    #data = table_data[1]

    pdf.set_font("helvetica",'B',10)
    
    col_width = (pdf.epw/4.7825) + 0.01
    line_height = pdf.font_size * 1.5
    table_width = 15
    margin_width = pdf.w - table_width
    center_table = margin_width/64
    x_start = center_table
    pdf.set_x(x_start)
    y1 = pdf.get_y()
    if x_start:
        x_left = x_start
    else:
        x_left = pdf.get_x()
    x_right = pdf.epw + x_left
    if x_start:
        pdf.set_x(x_start)
    for datum in header:
        #print(datum)
        if not isinstance(datum,str):
            datum = str(datum)
        if(topline):
            pdf.set_fill_color(155,155,155)
            pdf.multi_cell(col_width,line_height,datum,border=1,align='C',ln=3,max_line_height=pdf.font_size,fill=True)
            x_right = pdf.get_x()
        else:
            pdf.set_fill_color(255,255,255)
            pdf.multi_cell(col_width,line_height,datum,border=1,align='C',ln=3,max_line_height=pdf.font_size,fill=True)
            x_right = pdf.get_x()

    pdf.ln(line_height)
    y2 = pdf.get_y()
    pdf.line(x_left,y1,x_right,y1)
    pdf.line(x_left,y2,x_right,y2)
    if x_start:
        pdf.set_x(x_start)

def generateShape(pdf,x,y,i):
    if(i==0):
        pdf.circle(x-3,y-1,2.2,'FD')
    elif(i==1):
        pdf.regular_polygon(x-7,y+2,polyWidth=6,rotateDegrees=135,numSides=4,style='FD')
    elif(i==2):
        pdf.regular_polygon(x-6,y+2,polyWidth=6,rotateDegrees=90,numSides=3,style='FD')
    elif(i==3):
        pdf.regular_polygon(x-8,y+2,polyWidth=6,rotateDegrees=270,numSides=3,style='FD')
    elif(i==4):
        pdf.regular_polygon(x-7,y+2,polyWidth=6,rotateDegrees=180,numSides=4,style='FD')
    elif(i==5):
        pdf.regular_polygon(x-8,y+2,polyWidth=6,rotateDegrees=198,numSides=5,style='FD')
    elif(i==6):
        pdf.regular_polygon(x-8,y+2,polyWidth=6,rotateDegrees=180,numSides=6,style='FD')
    elif(i==7):
        pdf.regular_polygon(x-7,y+2,polyWidth=6,rotateDegrees=180,numSides=3,style='FD')
    elif(i==8):
        pdf.regular_polygon(x-7,y+2,polyWidth=6,rotateDegrees=0,numSides=3,style='FD')
    elif(i==9):
        pdf.regular_polygon(x-7,y+2,polyWidth=6,rotateDegrees=378,numSides=5,style='FD')
    elif(i==10):
        pdf.star(x-5,y-1,r_in=1,r_out=3,rotate_degrees=0,corners=3,style='FD')
    elif(i==11):
        pdf.star(x-5,y-1,r_in=1,r_out=3,rotate_degrees=0,corners=4,style='FD')
    elif(i==12):
        pdf.star(x-5,y-1,r_in=1,r_out=3,rotate_degrees=0,corners=5,style='FD')
    elif(i==13):
        pdf.star(x-5,y-1,r_in=1,r_out=3,rotate_degrees=0,corners=6,style='FD')

def placeShape(pdf,x,y,i):
    if(i==0):
        pdf.circle(x,y,2.2,'FD')
    elif(i==1):
        pdf.regular_polygon(x-3,y+3,polyWidth=6,rotateDegrees=135,numSides=4,style='FD')
    elif(i==2):
        pdf.regular_polygon(x-3,y+3,polyWidth=6,rotateDegrees=90,numSides=3,style='FD')
    elif(i==3):
        pdf.regular_polygon(x-3,y+3,polyWidth=6,rotateDegrees=270,numSides=3,style='FD')
    elif(i==4):
        pdf.regular_polygon(x-3,y+3,polyWidth=6,rotateDegrees=180,numSides=4,style='FD')
    elif(i==5):
        pdf.regular_polygon(x-3,y+3,polyWidth=6,rotateDegrees=198,numSides=5,style='FD')
    elif(i==6):
        pdf.regular_polygon(x-3,y+3,polyWidth=6,rotateDegrees=180,numSides=6,style='FD')
    elif(i==7):
        pdf.regular_polygon(x-3,y+3,polyWidth=6,rotateDegrees=180,numSides=3,style='FD')
    elif(i==8):
        pdf.regular_polygon(x-3,y+3,polyWidth=6,rotateDegrees=0,numSides=3,style='FD')
    elif(i==9):
        pdf.regular_polygon(x-3,y+3,polyWidth=6,rotateDegrees=378,numSides=5,style='FD')
    elif(i==10):
        pdf.star(x,y-1,r_in=1,r_out=3,rotate_degrees=0,corners=3,style='FD')
    elif(i==11):
        pdf.star(x,y,r_in=1,r_out=3,rotate_degrees=0,corners=4,style='FD')
    elif(i==12):
        pdf.star(x,y,r_in=1,r_out=3,rotate_degrees=0,corners=5,style='FD')
    elif(i==13):
        pdf.star(x,y,r_in=1,r_out=3,rotate_degrees=0,corners=6,style='FD')

def applyPitchEdits(pdf,pitcherlist,pitchershapelist):
    x = 25
    y = 210
    pdf.set_font('helvetica','B',17)
    pdf.text(45,60,"RHH")
    pdf.text(130,60,"Overall")
    pdf.text(222,60,"LHH")
    pdf.text(42,132,"In-Zone")
    pdf.text(128,132,"Out-Zone")
    pdf.text(212,132,"Two Strikes")
    pdf.set_font('helvetica','B',10)
    pdf.text(5,200,"Pitch Call:")
    pdf.set_fill_color(255,0,0)
    pdf.circle(27,199,2.2,'F')
    pdf.text(30,200,"Strike Call")
    pdf.set_fill_color(153,153,255)
    pdf.circle(52,199,2.2,'F')
    pdf.text(55,200,"Ball Call")
    pdf.set_fill_color(224,224,224)
    pdf.text(5,210,"Pitcher:")
    i = 0
    for pitcher in pitcherlist:
        pitchershapelist.append([pitcher,i])
        pdf.text(x,y,pitcher)
        generateShape(pdf,x,y,i)
        i+=1
        x+= len(pitcher) + 18
        #print(pitcher)
    #print(pitchershapelist)

#END FUNCDEF
#print(HitData)
def genStats(filestring,outputname_catcher):
    print(filestring)
    pd.options.display.max_rows = 100
    pd.options.display.max_columns = 100

    #END DEBUG SETTINGS

    HitData = pd.read_csv(filestring)

    #SPECIFIC ITEMS HERE

    BATTER_TEAM = "HOU_COU"
    TEAM_LOGO_FILE = "UH_Logo.png"
    WIDTH_ADJUSTMENT = 16
    HEIGHT_ADJUSTMENT = 16
    MinWidth= ((-17.04/2)) #Zone left in inches
    MaxWidth=((17.04/2)) #Zone right in inches
    MinHeight=((19.44)) #Zone bottom (Above home plate) in inches
    MaxHeight=((38.52)) #Zone top in inches
    MAX_BALL_PLACEMENT_HEIGHT = 45.20 #Excludes if too high for PDF placement
    MIN_BALL_PLACEMENT_HEIGHT = -14 #Excludes if too low for pdf placement
    MAX_BALL_PLACEMENT_WIDTH = 40#excludes if too much to the right
    MIN_BALL_PLACEMENT_WIDTH = -40 #excludes if too much to the left

    #END SPECIFIC ITEMS
    
    HitData = HitData.sort_values(by=["Catcher","Pitcher"])
    HitData = HitData.dropna(how='all')
    CatchData = HitData[["Catcher","CatcherTeam","Pitcher","PitchCall","PlateLocHeight","PlateLocSide","Strikes","BatterSide"]]
    #print(CatchData)
    #BatterData = BatterData[BatterData.BatterTeam == "HOU_COU"]
    #print(BatterData)
    try:
        DateString = HitData["Date"].values[0]
    except:
        DateString = "Date has error?"

    #PlayerData = pd.DataFrame(columns=["Batter","Plate App","Pitches","Hits","Strikeouts","Walks","Strikes","Swings","Whiffs","Chases","BABIP","HardHits","AvgEV","PitchType"])
    CatcherData = pd.DataFrame(columns=["CatcherName","CatcherTeam","Chances","ZoneStrike","StrikesStolen","StrikesLost","Score","PitchersFaced","RightArray","LeftArray","InZoneArray","OutZoneArray","TwoStrikeArray","OverallArray"])


    Balls = 0
    Strikes = 0
    Chances = 0
    index = -1
    Catcher = CatchData["Catcher"].values[0]
    CatcherTeam = CatchData["CatcherTeam"].values[0]
    PitchersFaced = []
    RightArray = []
    LeftArray = []
    InZoneArray = []
    OutZoneArray = []
    TwoStrikeArray = []
    OverallArray = []

    #GETTING OVERALL STATS FOR THE GAME
    while True:
        for row in CatchData["Catcher"]:
            try:
                index+=1
                if(Catcher != row):
                    ZoneStrikeCounter = 0
                    for i in range(0,len(InZoneArray)):
                        if(InZoneArray[i][1][0][0]=='S'):
                            ZoneStrikeCounter+=1

                    

                    ZoneStrikePercent = round(float(ZoneStrikeCounter/len(InZoneArray))*100,2) if len(InZoneArray)>0 else 0

                    StrikesStolenCounter = 0
                    for i in range(0,len(OutZoneArray)):
                        if(OutZoneArray[i][1][0][0]=='S'):
                            StrikesStolenCounter+=1

                    StrikesLostCounter = 0
                    for i in range(0,len(InZoneArray)):
                        if(InZoneArray[i][1][0][0]=='B'):
                            StrikesLostCounter +=1
                    
                    CatcherData = pd.concat([pd.DataFrame([[Catcher,CatcherTeam,Chances,ZoneStrikePercent,StrikesStolenCounter,StrikesLostCounter,StrikesStolenCounter-StrikesLostCounter,PitchersFaced,RightArray,LeftArray,InZoneArray,OutZoneArray,TwoStrikeArray,OverallArray]],columns=CatcherData.columns),CatcherData],ignore_index=True)
                    Strikes = 0
                    Balls = 0
                    Chances = 0
                    Catcher = CatchData["Catcher"].values[index]
                    CatcherTeam = CatchData["CatcherTeam"].values[index]
                    PitchersFaced = []
                    RightArray = []
                    LeftArray = []
                    OutZoneArray = []
                    InZoneArray = []
                    TwoStrikeArray = []
                    OverallArray = []

                PitchCallString = CatchData["PitchCall"].values[index]
                #Adding Chances
                if(PitchCallString == "StrikeCalled"):
                    Strikes+=1
                    Chances+=1
                elif(PitchCallString == "BallCalled"):
                    Balls+=1
                    Chances+=1
                elif(PitchCallString == "StrikeSwinging"):
                    Strikes+=1
                    Chances+=1
                else:
                    continue

                #Getting Pitchers
                PitcherString = CatchData["Pitcher"].values[index].split(",")[1][1]+"."+CatchData["Pitcher"].values[index].split(",")[0]
                #print(PitcherString)
                if PitcherString not in PitchersFaced:
                    PitchersFaced.append(PitcherString)

                PitchTriple = []
                #Gathering specific hit data to array
                PitchTriple.append([PitcherString])
                PitchTriple.append([PitchCallString])
                PlateWidth = float(CatchData["PlateLocSide"].values[index])
                PlateHeight = float(CatchData["PlateLocHeight"].values[index])
                PlateWidthIN = PlateWidth*12
                PlateHeightIN = PlateHeight*12
                PitchTriple.append([PlateWidth,PlateHeight])
                if(CatchData["BatterSide"].values[index]=="Left"):
                    LeftArray.append(PitchTriple)

                if(CatchData["BatterSide"].values[index]=="Right"):
                    RightArray.append(PitchTriple)

                if(CatchData["Strikes"].values[index]==2):
                    TwoStrikeArray.append(PitchTriple)

                if(MinWidth>PlateWidthIN or PlateWidthIN>MaxWidth) or (MinHeight>=PlateHeightIN or PlateHeightIN>=MaxHeight):
                    OutZoneArray.append(PitchTriple)
                elif(MinWidth<=PlateWidthIN or PlateWidthIN<=MaxWidth) or (MinHeight<PlateHeightIN or PlateHeightIN<MaxHeight):
                    InZoneArray.append(PitchTriple)
                
                OverallArray.append(PitchTriple)
                
                
            except Exception as e:
                print(e)
                pass
        break

    #PLACING FINAL CATCH
    #Getting Pitchers
    PitcherString = CatchData["Pitcher"].values[index].split(",")[1][1]+"."+CatchData["Pitcher"].values[index].split(",")[0]
    #print(PitcherString)
    if PitcherString not in PitchersFaced:
        PitchersFaced.append(PitcherString)

    PitchTriple = []
    #Gathering specific hit data to array
    PitchTriple.append([PitcherString])
    PitchTriple.append([PitchCallString])
    PlateWidth = float(CatchData["PlateLocSide"].values[index])
    PlateHeight = float(CatchData["PlateLocHeight"].values[index])
    PlateWidthIN = PlateWidth*12
    PlateHeightIN = PlateHeight*12
    PitchTriple.append([PlateWidth,PlateHeight])
    if(CatchData["BatterSide"].values[index]=="Left"):
        LeftArray.append(PitchTriple)

    if(CatchData["BatterSide"].values[index]=="Right"):
        RightArray.append(PitchTriple)

    if(CatchData["Strikes"].values[index]==2):
        TwoStrikeArray.append(PitchTriple)

    if(MinWidth>PlateWidthIN or PlateWidthIN>MaxWidth) or (MinHeight>=PlateHeightIN or PlateHeightIN>=MaxHeight):
        OutZoneArray.append(PitchTriple)
    elif(MinWidth<=PlateWidthIN or PlateWidthIN<=MaxWidth) or (MinHeight<PlateHeightIN or PlateHeightIN<MaxHeight):
        InZoneArray.append(PitchTriple)
    
    OverallArray.append(PitchTriple)
    ZoneStrikeCounter = 0
    for i in range(0,len(InZoneArray)):
        if(InZoneArray[i][1][0][0]=='S'):
            ZoneStrikeCounter+=1

    

    ZoneStrikePercent = round(float(ZoneStrikeCounter/len(InZoneArray))*100,2) if len(InZoneArray)>0 else 0

    StrikesStolenCounter = 0
    for i in range(0,len(OutZoneArray)):
        if(OutZoneArray[i][1][0][0]=='S'):
            StrikesStolenCounter+=1

    StrikesLostCounter = 0
    for i in range(0,len(InZoneArray)):
        if(InZoneArray[i][1][0][0]=='B'):
            StrikesLostCounter +=1
    
    CatcherData = pd.concat([pd.DataFrame([[Catcher,CatcherTeam,Chances,ZoneStrikePercent,StrikesStolenCounter,StrikesLostCounter,StrikesStolenCounter-StrikesLostCounter,PitchersFaced,RightArray,LeftArray,InZoneArray,OutZoneArray,TwoStrikeArray,OverallArray]],columns=CatcherData.columns),CatcherData],ignore_index=True)
    Strikes = 0
    Balls = 0
    Chances = 0
    Catcher = CatchData["Catcher"].values[index]
    CatcherTeam = CatchData["CatcherTeam"].values[index]
    PitchersFaced = []
    RightArray = []
    LeftArray = []
    OutZoneArray = []
    InZoneArray = []
    TwoStrikeArray = []
    OverallArray = []

    #print(CatcherData)

    CatcherData = CatcherData.iloc[::-1].reset_index(drop=True)
    FourSliceStrikeArray = [[35,75],[122,75],[212,75],[35,145],[122,145],[212,145]]
    FourSliceOriginArray = [[51.25,109],[138.25,109],[228.25,109],[51.25,179],[138.25,179],[228.25,179]]
    ABIndexCounter = 0
    #PUTTING ON PDF
    index = -1
    pdf = FPDF('L','mm','Letter')
    pdf.set_line_width(0.5)
    for row in CatcherData["CatcherName"]:
        pitchershapelist=[]
        index+=1
        pdf.add_page()
        pdf.set_font('helvetica','B',20)
        pdf.set_fill_color(200,16,46)
        pdf.image(os.getcwd()+f"\\ImgFiles\\{TEAM_LOGO_FILE}",10,8,20)
        pdf.cell(0,12,CatcherData["CatcherName"].values[index].split(",")[1] + " " + CatcherData["CatcherName"].values[index].split(",")[0] + " - " +CatcherData["CatcherTeam"].values[index],False,1,'C')
        pdf.set_font('helvetica','B',15)
        pdf.cell(pdf.epw+8,8,DateString,False,ln=True,align='R')
        pdf.set_font('helvetica','B',15)
        pdf.set_text_color(255,255,255)
        pdf.set_margins(2,10)
        pdf.set_line_width(1)
        curY=pdf.get_y()
        pdf.cell(pdf.epw,21,"",1,1,'C') #small box
        pdf.set_y(pdf.get_y()+2)
        pdf.cell(pdf.epw,142,"",1,1,'C') #large box
        pdf.set_line_width(0.5)
        pdf.set_x(0)
        pdf.set_y(curY+2)
        pdf.set_margins(4,10)
        pdf.cell(0,6,"Catcher Report",True,1,'C',fill=True)
        pdf.set_text_color(0,0,0)
        pdf.set_margins(10,10)
        create_table_statline([["Chances","Zone Strike %","Strikes Stolen (+)","Strikes Lost (-)","Score"]],True,pdf)
        create_table_statline([[CatcherData["Chances"].values[index],CatcherData["ZoneStrike"].values[index],CatcherData["StrikesStolen"].values[index],CatcherData["StrikesLost"].values[index],"???"]],False,pdf)
        #create_table_statline([CatcherData.loc[index],False,pdf)
        #create_table_statline([PlayerData.loc[index][2:]],False,pdf)
        pdf.set_font('helvetica','B',10)
        #print(pdf.epw)
        pdf.line(pdf.epw/2+9-43.23,67,pdf.epw/2+9-43.23,190) #vert line 1
        pdf.line(pdf.epw/2+9+43.23,67,pdf.epw/2+9+43.23,190) #vert line 2
        pdf.line(10,125,270,125)#horiz line
        #Putting in at bats
        ABFours = 0
        applyPitchEdits(pdf,CatcherData["PitchersFaced"].values[index],pitchershapelist)
        #GO THROUGH FOUR AT BATS
        CatcherSixes=0
        ArrStrings = ["RightArray","OverallArray","LeftArray","InZoneArray","OutZoneArray","TwoStrikeArray"]
        while CatcherSixes<6:
            
            pdf.set_xy(FourSliceStrikeArray[CatcherSixes][0],FourSliceStrikeArray[CatcherSixes][1])
            pdf.image(os.getcwd()+"\\ImgFiles\\StrikeZone.png",None,None,32,35.55) #placing strikezone
            pdf.set_xy(FourSliceOriginArray[CatcherSixes][0],FourSliceOriginArray[CatcherSixes][1])
            for throw in CatcherData[ArrStrings[CatcherSixes]].values[index]:
                #print(throw,ArrStrings[CatcherSixes])
                width = (throw[2][0]*12*25.4)/WIDTH_ADJUSTMENT
                height = ((throw[2][1]*12*25.4) - (19.44*25.4))/HEIGHT_ADJUSTMENT

                if(math.isnan(height) or math.isnan(width)):
                    continue
                elif(height>MAX_BALL_PLACEMENT_HEIGHT):
                    continue
                elif(height<MIN_BALL_PLACEMENT_HEIGHT):
                    continue
                elif(width<MIN_BALL_PLACEMENT_WIDTH):
                    continue
                elif(width>MAX_BALL_PLACEMENT_WIDTH):
                    continue

                if throw[1][0][0]=='S':
                    pdf.set_fill_color(255,0,0)
                elif throw[1][0][0]=='B':
                    pdf.set_fill_color(155,155,255)

                pitcherID = 0
                for pitcher in pitchershapelist:
                    if pitcher[0]==throw[0][0]:
                        pitcherID=pitcher[1]
                placeShape(pdf,pdf.get_x()+width,pdf.get_y()-height,pitcherID)
                
                #pdf.circle(pdf.get_x()+width,pdf.get_y()-height,radius=2.3,style='FD')
            CatcherSixes+=1


    print("Done")
    if outputname_catcher!="":
        pdf.output(outputname_catcher)

print("Generator Imported")
#genStats("Baseball.csv","hi.pdf")
