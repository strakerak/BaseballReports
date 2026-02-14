import numpy as np
import pandas as pd
from collections import defaultdict
from fpdf import FPDF
import math
import sys
import os
#DEBUG SETTINGS


def create_table_statline(table_data,topline,pdf,title='',data_size=10,title_size=12,align_data='C',cell_width='even',x_start='C',emphasize_data=[],emphasize_style=None,emphasize_color=(0,0,0)):
    #print(table_data[0])
    header = table_data[0]
    #data = table_data[1]

    pdf.set_font("helvetica",'B',10)
    
    col_width = (pdf.epw/13.4) + 0.015
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

def create_table_abline(pdf,table_data,topline,x_val):
    #print(x_val,pdf.get_y()+6)
    pdf.set_y(pdf.get_y()+4.0)
    pdf.set_x(x_val)
    header = table_data[0]
    col_width = 17.5
    line_height=pdf.font_size*1.1
    table_width = 5
    margin_width = 5
    pdf.set_x(pdf.get_x())
    for datum in header:
        if not isinstance(datum,str):
            datum = str(datum)
        if topline:
            pdf.set_fill_color(155,155,155)
            pdf.multi_cell(col_width,line_height,datum,border=1,align='C',ln=3,max_line_height=pdf.font_size,fill=True)
        else:
            pdf.set_fill_color(255,255,255)
            pdf.multi_cell(col_width,line_height,datum,border=1,align='C',ln=3,max_line_height=pdf.font_size,fill=True)
    pdf.set_y(pdf.get_y())
    pass

def applyPitchEdits(pdf):
    pdf.text(5,58,"Pitch Call:")
    pdf.circle(25,57,2.2,style=None)
    pdf.text(28,58,"Ball")
    pdf.regular_polygon(35.75,59.5,polyWidth=5,rotateDegrees=198,numSides=5,style=None)
    pdf.text(42,58,"FoulBallNotFieldable")
    pdf.regular_polygon(77,59.25,polyWidth=6,rotateDegrees=90,numSides=3,style=None)
    pdf.text(85,58,"In Play")
    pdf.regular_polygon(99,60.5,polyWidth=6,rotateDegrees=270,numSides=3,style=None)
    pdf.text(105,58,"Strike Call")
    pdf.regular_polygon(125,60.5,polyWidth=7,rotateDegrees=135,numSides=4,style=None)
    pdf.text(132,58,"Strike Swinging")
    pdf.text(165,58,"BallInDirt")
    pdf.text(252,58,"Pitch Type: ")
    pdf.set_fill_color(255,0,0)
    pdf.circle(254,62,2.2,'F')
    pdf.text(257,63,"Fastball")
    pdf.set_fill_color(0,255,0)
    pdf.circle(254,67,2.2,'F')
    pdf.text(257,68,"Changeup")
    pdf.set_fill_color(204,204,0)
    pdf.circle(254,72,2.2,'F')
    pdf.text(257,73,"Slider")
    pdf.set_fill_color(255,204,153)
    pdf.circle(254,77,2.2,'F')
    pdf.text(257,78,"Cutter")
    pdf.set_fill_color(255,0,165)
    pdf.circle(254,82,2.2,'F')
    pdf.text(257,83,"Sinker")
    pdf.set_fill_color(255,165,0)
    pdf.circle(254,87,2.2,'F')
    pdf.text(257,88,"Curveball")
    pdf.set_fill_color(229,204,255)
    pdf.circle(254,92,2.2,'F')
    pdf.text(257,93,"Splitter")
    pdf.set_fill_color(153,153,255)
    pdf.circle(254,97,2.2,'F')
    pdf.text(257,98,"Knuckleball")
    pdf.set_fill_color(224,224,224)
    pdf.circle(254,102,2.2,'F')
    pdf.text(257,103,"Undefined")
    pdf.set_fill_color(224,224,224)
    pdf.circle(254,107,2.2,'F')
    pdf.text(257,108,"Other")

#END FUNCDEF
def genStats(filestring,outputname_batter):
    #SPECIFIC ITEMS HERE
    BATTER_TEAM = "HOU_COU"
    TEAM_LOGO_FILE = "UH_Logo.png"
    WIDTH_ADJUSTMENT = 16
    HEIGHT_ADJUSTMENT = 16
    MinWidth= ((-17.04/2)) #Zone left in inches
    MaxWidth=((17.04/2)) #Zone right in inches
    MinHeight=((19.44)) #Zone bottom (Above home plate) in inches
    MaxHeight=((38.52)) #Zone top in inches
    MAX_BALL_PLACEMENT_HEIGHT = 32.70 #Excludes if too high for PDF placement
    MIN_BALL_PLACEMENT_HEIGHT = -13 #Excludes if too low for pdf placement
    MAX_BALL_PLACEMENT_WIDTH = 35 #excludes if too much to the right
    MIN_BALL_PLACEMENT_WIDTH = -35 #excludes if too much to the left
    #END SPECIFIC ITEMS
    print(filestring)
    pd.options.display.max_rows = 100
    pd.options.display.max_columns = 100

    #END DEBUG SETTINGS

    HitData = pd.read_csv(filestring)

    #FUNCDEF

    
    HitData = HitData.sort_values(by=["Batter","PitchNo"])
    HitData = HitData.dropna(how='all')
    BatterData = HitData[["Batter","BatterTeam","PitchNo","PitchofPA","PAofInning","TaggedPitchType","AutoPitchType","PitchCall","KorBB","TaggedHitType","PlayResult","ExitSpeed","Angle","Direction","Date","Time","ZoneSpeed","PlateLocHeight","PlateLocSide"]]
    BatterData = BatterData[BatterData.BatterTeam == f"{BATTER_TEAM}"]
    #print(BatterData)
    try:
        DateString = HitData["Date"].values[0].split("-")
        DateString = DateString[1] + "/" + DateString[2] + "/" + DateString[0]
    except:
        DateString = "Date has error?"

    #PlayerData = pd.DataFrame(columns=["Batter","Plate App","Pitches","Hits","Strikeouts","Walks","Strikes","Swings","Whiffs","Chases","BABIP","HardHits","AvgEV","PitchType"])
    PlayerData = pd.DataFrame(columns=["Batter","Balls","Plate Appearances","Pitches","Pitches Per Plate App","Hits","Strikeouts","Walks","Strikes","Swings","Whiffs","Chases","BIP","AverageEV","HardHit (BIP/BIP>95)","Seen"])


    plateApp=0
    Batter = ""
    Pitches = 0
    Hits = 0
    Strikeouts = 0
    Balls = 0
    Walks = 0
    Strikes = 0
    Swings = 0
    Whiffs = 0
    Chases = 0
    BABIP = 0
    HardHits = 0
    AvgEV = 0
    PitchType = ""
    index = -1
    PPA = 0
    FoulBalls = 0
    StrikeSwings = 0
    EVCount = 0
    EVTot = 0
    HardAttempts = 0
    HardHits = 0
    Batter = BatterData["Batter"].values[0]

    PlateAppearanceCounter = {}

    #GETTING OVERALL STATS FOR THE GAME
    while True:
        for row in BatterData["Batter"]:
            try:
                index+=1
                if(Batter != row):
                    PPA = round(Pitches/PlateAppearanceCounter[Batter],2)
                    PA = PlateAppearanceCounter[Batter]
                    SwingString = f"{Swings}/{Pitches}"
                    WhiffString = f"{Whiffs}/{Swings}"
                    StrikeString = f"{Strikes}/{Pitches}"
                    BABIPString = f"{BABIP}/{Swings}"
                    HitString = f"{Hits}/{BABIP}"
                    HardHitString = f"{HardHits}/{BABIP}"
                    SeenString = "---"
                    AvgEV = round(EVTot/EVCount,2) if EVCount>0 else 0
                    #NewBatterData = {"Batter":Batter,"Pitches":Pitches,"Strikeouts":Strikeouts,"Walks":Walks,"PA":PA,"PPA":PPA,"Strikes":Strikes,"Balls":Balls,"BIP":BABIP,"Swings":Swings,"Whiffs":Whiffs,"Hits":Hits,"AverageEV":AvgEV,"HardHits":HardHitString,"Seen":SeenString,"Chases":Chases}#,"Strikes":Strikes,"Balls":Balls}
                    PlayerData = pd.concat([pd.DataFrame([[Batter,Balls,PA,Pitches,PPA,Hits,Strikeouts,Walks,StrikeString,SwingString,WhiffString,Chases,BABIPString,HardHitString,AvgEV,Balls]],columns=PlayerData.columns),PlayerData],ignore_index=True)
                    Pitches = 0
                    Strikeouts = 0
                    Walks = 0
                    BABIP = 0
                    Strikes = 0
                    Hits = 0
                    Balls = 0
                    FoulBalls = 0
                    Swings = 0
                    StrikeSwings = 0
                    Whiffs = 0
                    EVCount = 0
                    EVTot = 0
                    AvgEV = 0
                    HardAttempts = 0
                    HardHits = 0
                    Batter = BatterData["Batter"].values[index]
                if(index > 0 and BatterData["PitchofPA"].values[index]<=BatterData["PitchofPA"].values[index-1]):
                    PlateAppearanceCounter[Batter] = 1 + PlateAppearanceCounter.get(Batter,0)
                elif(index==0):
                    PlateAppearanceCounter[Batter] = 1 + PlateAppearanceCounter.get(Batter,0)
                Pitches+=1
                if(BatterData["KorBB"].values[index]=="Strikeout"):
                    Strikeouts+=1
                elif(BatterData["KorBB"].values[index]=="Walk"):
                    Walks+=1

                if(BatterData["PitchCall"].values[index] == "StrikeCalled"):
                    Strikes+=1
                elif(BatterData["PitchCall"].values[index] == "BallCalled"):
                    Balls+=1
                elif(BatterData["PitchCall"].values[index] == "FoulBallNotFieldable"):
                    FoulBalls+=1
                    #Swings+=1
                elif(BatterData["PitchCall"].values[index] == "StrikeSwinging"):
                    Swings+=1
                    Strikes+=1
                    Whiffs+=1
                elif(BatterData["PitchCall"].values[index]=="InPlay"):
                    Swings+=1
                if(BatterData["TaggedHitType"].values[index] != "Undefined"):
                    BABIP+=1
                    if(not np.isnan(BatterData["ExitSpeed"].values[index]) and float(BatterData["ExitSpeed"].values[index])>95.0):
                        HardHits+=1
                if(BatterData["PlayResult"].values[index]!="Out" and BatterData["PlayResult"].values[index] != "Undefined" and BatterData["PlayResult"].values[index]!="CaughtStealing"):
                    Hits+=1
                    #if(not np.isnan(BatterData["ExitSpeed"].values[index]) and float(BatterData["ExitSpeed"].values[index])>95.0):
                    #    HardHits+=1
                if(not np.isnan(BatterData["ExitSpeed"].values[index]) and float(BatterData["ExitSpeed"].values[index])>95.0):
                        HardAttempts+=1 #Raising this questions, since ablls in play SHOULD be around "BallInPlay" or JUST successful hits. 
                if(not np.isnan(BatterData["ExitSpeed"].values[index])):
                    EVTot += float(BatterData["ExitSpeed"].values[index])
                    EVCount+=1
            except Exception as e:
                print(e)
                pass
        break

    #PLACING FINAL BATTER
    PPA = round(Pitches/PlateAppearanceCounter[Batter],2)
    PA = PlateAppearanceCounter[Batter]
    SwingString = f"{Swings}/{Pitches}"
    WhiffString = f"{Whiffs}/{Swings}"
    StrikeString = f"{Strikes}/{Pitches}"
    BABIPString = f"{BABIP}/{Swings}"
    HitString = f"{Hits}/{BABIP}"
    HardHitString = f"{HardHits}/{BABIP}"
    SeenString = "0/0/0"
    AvgEV = round(EVTot/EVCount,2) if EVCount>0 else 0
    PlayerData = pd.concat([pd.DataFrame([[Batter,Balls,PA,Pitches,PPA,Hits,Strikeouts,Walks,StrikeString,SwingString,WhiffString,Chases,BABIPString,HardHitString,AvgEV,SeenString]],columns=PlayerData.columns),PlayerData],ignore_index=True)
    Pitches = 0
    Strikeouts = 0
    Walks = 0
    BABIP = 0
    Strikes = 0
    Hits = 0
    Balls = 0
    FoulBalls = 0
    Swings = 0
    StrikeSwings = 0
    Whiffs = 0
    EVCount = 0
    EVTot = 0
    AvgEV = 0
    HardAttempts = 0
    HardHits = 0
    Batter = BatterData["Batter"].values[index]



    #GETTING OVERALL STATS FOR EACH AT BAT
    #Pitches, Swings, Whiffs, Chases, Result of BIP, Where the hit went, where each pitch was in the zone (tuple), pitch type
    ABData = pd.DataFrame(columns = ["Batter","Pitches","Swings","Whiffs","Chases","PitchTypes","ZoneArray","FieldLanding","PitchResult","PlayResult","ExitVel","ChasesAttempted","Exclude"])
    PlayerIndex = 0
    index = -1
    Swings = 0
    Whiffs = 0
    Chases = 0
    ChasesAttempted = 0
    Pitches = 0
    ExitVel = 0
    PitchTypes = [] #Handle this for PDF Finale, collect these, put them in the final, or make the graph then and there. Fastball, Changeup, or Slider
    PitchResult = []
    ZoneArray = [] #[Width,Height]
    FieldLanding = [] #I think this is three dimensional
    Strikes = 0
    BABIP = 0
    Exclude = False
    PlayResult = ""
    Batter = BatterData["Batter"].values[0]
    for row in BatterData["Batter"]:
        index+=1
        if(Batter!=row):
            #print("NEW BATTER, PREVIOUS WAS ",Batter," AND HE HAD ",Pitches, "AND TOTAL",PlayerData["Pitches"].values[10-PlayerIndex])
            ABData = pd.concat([pd.DataFrame([[Batter,Pitches,Swings,Whiffs,Chases,PitchTypes,ZoneArray,FieldLanding,PitchResult,PlayResult,ExitVel,ChasesAttempted,Exclude]],columns=ABData.columns),ABData],ignore_index=True)
            PlayerIndex+=1
            Pitches = 0
            Whiffs = 0
            Swings = 0
            ChasesAttempted = 0
            Chases = 0
            ExitVel = 0
            PitchTypes = []
            ZoneArray = []
            FieldLanding = []
            PitchResult = []
            Exclude = False
            Batter = BatterData["Batter"].values[index]

        elif(index > 0 and BatterData["PitchofPA"].values[index]<=BatterData["PitchofPA"].values[index-1]):
            #print("NEW AT BAT FOR ",BatterData["Batter"].values[index],Pitches)
            ABData = pd.concat([pd.DataFrame([[Batter,Pitches,Swings,Whiffs,Chases,PitchTypes,ZoneArray,FieldLanding,PitchResult,PlayResult,ExitVel,ChasesAttempted,Exclude]],columns=ABData.columns),ABData],ignore_index=True)
            Pitches = 0
            Whiffs = 0
            Swings = 0
            ChasesAttempted = 0
            Chases = 0
            ExitVel = 0
            PitchTypes = []
            ZoneArray = []
            FieldLanding = []
            PitchResult = []
            Exclude = False

        #print(BatterData["Batter"].values[index],BatterData["PitchCall"].values[index])
        if(BatterData["PitchCall"].values[index] == "StrikeCalled"):
            Strikes+=1
            PitchResult.append("Strike")
        elif(BatterData["PitchCall"].values[index] == "BallCalled"):
            Balls+=1
            PitchResult.append("Ball")
        elif(BatterData["PitchCall"].values[index] == "FoulBallNotFieldable"):
            FoulBalls+=1
            PitchResult.append("FoulBallNF")
            #Swings+=1
            if((MinWidth>BatterData["PlateLocSide"].values[index]*12 or BatterData["PlateLocSide"].values[index]*12>MaxWidth) or (MinHeight>BatterData["PlateLocHeight"].values[index]*12 or BatterData["PlateLocHeight"].values[index]*12>MaxHeight)):
                ChasesAttempted+=1
        elif(BatterData["PitchCall"].values[index] == "FoulBall"):
            FoulBalls+=1
            PitchResult.append("FoulBallNF")
            #Swings+=1
            if((MinWidth>BatterData["PlateLocSide"].values[index]*12 or BatterData["PlateLocSide"].values[index]*12>MaxWidth) or (MinHeight>BatterData["PlateLocHeight"].values[index]*12 or BatterData["PlateLocHeight"].values[index]*12>MaxHeight)):
                ChasesAttempted+=1
        elif(BatterData["PitchCall"].values[index] == "StrikeSwinging"):
            Swings+=1
            Strikes+=1
            Whiffs+=1
            PitchResult.append("StrikeSwinging")
            if((MinWidth>BatterData["PlateLocSide"].values[index]*12 or BatterData["PlateLocSide"].values[index]*12>MaxWidth) or (MinHeight>BatterData["PlateLocHeight"].values[index]*12 or BatterData["PlateLocHeight"].values[index]*12>MaxHeight)):
                ChasesAttempted+=1
        elif(BatterData["PitchCall"].values[index]=="InPlay"):
            Swings+=1
            PitchResult.append("InPlay")
            if((MinWidth>BatterData["PlateLocSide"].values[index]*12 or BatterData["PlateLocSide"].values[index]*12>MaxWidth) or (MinHeight>BatterData["PlateLocHeight"].values[index]*12 or BatterData["PlateLocHeight"].values[index]*12>MaxHeight)):
                ChasesAttempted+=1
        elif(BatterData["PitchCall"].values[index]=="Undefined"):
            PitchResult.append("Undefined")
        elif(BatterData["PitchCall"].values[index]=="BallInDirt"):
            Pitchresult.append("BallInDirt")
        elif(BatterData["PitchCall"].values[index] == "BallIntentional"):
            Balls+=1
            PitchResult.append("Ball")
        elif(BatterData["PitchCall"].values[index]=="HitByPitch"):
            PitchResult.append("HitByPitch")
        
        if(BatterData["TaggedHitType"].values[index] != "Undefined"):
            BABIP+=1
            #PitchResult.append("InPlay")

        PitchTypes.append(BatterData["TaggedPitchType"].values[index])
        ZoneArray.append([BatterData["PlateLocSide"].values[index],BatterData["PlateLocHeight"].values[index]])
        if((MinWidth>BatterData["PlateLocSide"].values[index]*12 or BatterData["PlateLocSide"].values[index]*12>MaxWidth) or (MinHeight>BatterData["PlateLocHeight"].values[index]*12 or BatterData["PlateLocHeight"].values[index]*12>MaxHeight)):
            Chases+=1
            PlayerData.loc[PlayerData["Batter"]==Batter,["Chases"]]+=1
            #print(Batter,"Chase",MinWidth,MaxWidth,MinHeight,MaxHeight,BatterData["PlateLocSide"].values[index]*12,BatterData["PlateLocHeight"].values[index]*12,Exclude)
        else:
            pass
            #Chases+=1
            #print(Batter,"Chase",MinWidth,MaxWidth,MinHeight,MaxHeight,BatterData["PlateLocSide"].values[index]*12,BatterData["PlateLocHeight"].values[index]*12)
        if(BatterData["PlayResult"].values[index]!="Undefined"):
            PlayResult = BatterData["PlayResult"].values[index]
            ExitVel = round(BatterData["ExitSpeed"].values[index],2)
        elif(BatterData["PlayResult"].values[index]=="Undefined" and BatterData["KorBB"].values[index]!="Undefined"):
            PlayResult = BatterData["KorBB"].values[index]
        
        #print(BatterData["Batter"].values[index],BatterData["PitchofPA"].values[index])
        Pitches+=1
            
        
        #print(BatterData["Batter"].values[index])


    #FINAL AB HANDLED
    ABData = pd.concat([pd.DataFrame([[Batter,Pitches,Swings,Whiffs,Chases,PitchTypes,ZoneArray,FieldLanding,PitchResult,PlayResult,ExitVel,ChasesAttempted,Exclude]],columns=ABData.columns),ABData],ignore_index=True)

    ABData = ABData.iloc[::-1].reset_index(drop=True)
    PlayerData = PlayerData.iloc[::-1].reset_index(drop=True)

    FourSliceArray = [[30,60],[170,60],[30,130],[170,130]]
    FourSliceStrikeArray = [[20,75],[160,75],[20,145],[160,145]]
    FourSliceOriginArray = [[36.25,109],[176.25,109],[36.25,179],[176.25,179]]
    ABIndexCounter = 0
    #PUTTING ON PDF
    index = -1
    pdf = FPDF('L','mm','Letter')
    pdf.set_line_width(0.5)
    for row in PlayerData["Batter"]:
        CurAB=1
        index+=1
        PACount = PlayerData["Plate Appearances"].values[index]
        while(PACount>0):
            pdf.add_page()
            pdf.set_font('helvetica','B',20)
            pdf.set_fill_color(200,16,46)
            pdf.image(os.getcwd()+f"\\ImgFiles\\{TEAM_LOGO_FILE}",10,8,20)
            pdf.cell(0,12,PlayerData["Batter"].values[index].split(",")[1] + " " + PlayerData["Batter"].values[index].split(",")[0] + " - Post Game Hitter Report",False,1,'C')
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
            pdf.cell(0,6,"Post Game Stat Line",True,1,'C',fill=True)
            pdf.set_text_color(0,0,0)
            pdf.set_margins(10,10)
            create_table_statline([["PA","Pitches","PPA","Hits","Strikeouts","Walks","Strikes","Swings","Whiffs","Chases","BIP","HardHit","AvgEV","Balls"]],True,pdf)
            create_table_statline([PlayerData.loc[index][2:]],False,pdf)
            pdf.set_font('helvetica','B',10)
            pdf.line(pdf.epw/2+9,67,pdf.epw/2+9,190) #vert line in center
            pdf.line(10,125,270,125)#horiz line in center
            #Putting in at bats
            ABFours = 0
            applyPitchEdits(pdf)
            #GO THROUGH FOUR AT BATS
            while row==ABData["Batter"].values[ABIndexCounter]:
                #print(CurAB,ABFours)
                if(ABFours>3):
                    #print("new page")
                    break
                pdf.set_xy(FourSliceArray[ABFours][0],FourSliceArray[ABFours][1])
                if(ABData["ExitVel"].values[ABIndexCounter]==0):
                    CellString = f"PA: {CurAB} " + ABData["PlayResult"].values[ABIndexCounter]+ " (No EV)"
                else:
                    CellString = f"PA: {CurAB} " + ABData["PlayResult"].values[ABIndexCounter]+" "+ "("+str(ABData["ExitVel"].values[ABIndexCounter])+" mph)"
                pdf.set_fill_color(200,16,46)
                pdf.set_text_color(255,255,255)
                pdf.cell(70,4,CellString,True,0,'C',fill=True)
                pdf.set_text_color(0,0,0)
                pdf.set_fill_color(155,155,155)
                pdf.set_x(FourSliceArray[ABFours][0])
                create_table_abline(pdf,[["Pitches","Swings","Whiffs","Chases"]],True,pdf.get_x())
                pdf.set_x(FourSliceArray[ABFours][0])
                create_table_abline(pdf,[[str(ABData["Pitches"].values[ABIndexCounter]),str(str(ABData["Swings"].values[ABIndexCounter])+"/"+str(ABData["Pitches"].values[ABIndexCounter])),str(str(ABData["Whiffs"].values[ABIndexCounter])+"/"+str(ABData["Swings"].values[ABIndexCounter])),str(str(ABData["ChasesAttempted"].values[ABIndexCounter])+"/"+str(ABData["Chases"].values[ABIndexCounter]))]],False,pdf.get_x())
                pdf.set_xy(FourSliceStrikeArray[ABFours][0],FourSliceStrikeArray[ABFours][1])
                pdf.image(os.getcwd()+"\\ImgFiles\\StrikeZone.png",None,None,32,35.55) #placing strikezone
                pdf.image(os.getcwd()+"\\ImgFiles\\Field.png",pdf.get_x()+50,pdf.get_y()-30,37.54,32)
                #Handling each pitch in the bat
                pdf.set_fill_color(0,0,0)
                pdf.set_xy(FourSliceOriginArray[ABFours][0],FourSliceOriginArray[ABFours][1])
                for i in range(0,len(ABData["ZoneArray"].values[ABIndexCounter])):
                    width = (ABData["ZoneArray"].values[ABIndexCounter][i][0]*12*25.4)/WIDTH_ADJUSTMENT
                    height = ((ABData["ZoneArray"].values[ABIndexCounter][i][1]*12*25.4)-(19.44*25.4))/HEIGHT_ADJUSTMENT
                    #print(width,height,ABData["Batter"].values[ABIndexCounter])
                    if(math.isnan(height) or math.isnan(width)):
                        #print("NAN")
                        continue
                    elif(height>MAX_BALL_PLACEMENT_HEIGHT):
                        #print("EXCLUDING BALL",height,width,ABData["Batter"].values[ABIndexCounter])
                        continue
                    elif(height<MIN_BALL_PLACEMENT_HEIGHT):
                        #print("HEIGHT LESS ZERO",height,ABData["Batter"].values[ABIndexCounter])
                        continue
                    elif(width<MIN_BALL_PLACEMENT_WIDTH):
                        #print("WAY TO THE LEFT",width,ABData["Batter"].values[ABIndexCounter])
                        continue
                    elif(width>MAX_BALL_PLACEMENT_WIDTH):
                        #print("WAY TO THE RIGHT",width,ABData["Batter"].values[ABIndexCounter])
                        continue

                    
                    if(ABData["PitchTypes"].values[ABIndexCounter][i]=="Fastball"):
                        pdf.set_fill_color(255,0,0)
                    elif(ABData["PitchTypes"].values[ABIndexCounter][i]=="ChangeUp"):
                        pdf.set_fill_color(0,255,0)
                    elif(ABData["PitchTypes"].values[ABIndexCounter][i]=="Slider"):
                        pdf.set_fill_color(204,204,0)
                    elif(ABData["PitchTypes"].values[ABIndexCounter][i]=="Curveball"):
                        pdf.set_fill_color(255,165,0)
                    elif(ABData["PitchTypes"].values[ABIndexCounter][i]=="Sinker"):
                        pdf.set_fill_color(255,0,165)
                    elif(ABData["PitchTypes"].values[ABIndexCounter][i]=="Splitter"):
                        pdf.set_fill_color(229,204,255)
                    elif(ABData["PitchTypes"].values[ABIndexCounter][i]=="Cutter"):
                        pdf.set_fill_color(255,204,153)
                    elif(ABData["PitchTypes"].values[ABIndexCounter][i]=="Knuckleball"):
                        pdf.set_fill_color(153,153,255)
                    elif(ABData["PitchTypes"].values[ABIndexCounter][i]=="Other" or ABData["PitchTypes"].values[ABIndexCounter][i]=="Undefined"):
                        pdf.set_fill_color(224,224,224)
                    #pdf.set_font('helvetica','',3)
                    
                    #print(pdf.get_x(),pdf.get_y())
                    #print(ABIndexCounter, len(ABData["PitchTypes"].values[ABIndexCounter]),len(ABData["PitchResult"].values[ABIndexCounter]))
                    if(ABData["PitchResult"].values[ABIndexCounter][i]=="Ball"):
                        pdf.circle(pdf.get_x()+width,pdf.get_y()-height,radius=2.3,style='FD')
                    elif(ABData["PitchResult"].values[ABIndexCounter][i]=="InPlay"):
                        pdf.regular_polygon(pdf.get_x()+width-3,pdf.get_y()-height+3,polyWidth=6,rotateDegrees=90,numSides=3,style='FD')
                        pass
                    elif(ABData["PitchResult"].values[ABIndexCounter][i]=="Strike"):
                        pdf.regular_polygon(pdf.get_x()+width-3,pdf.get_y()-height+3,polyWidth=6,rotateDegrees=270,numSides=3,style='FD')
                    elif(ABData["PitchResult"].values[ABIndexCounter][i]=="StrikeSwinging"):
                        pdf.regular_polygon(pdf.get_x()+width-3,pdf.get_y()-height+3,polyWidth=6,rotateDegrees=135,numSides=4,style='FD')
                    elif(ABData["PitchResult"].values[ABIndexCounter][i]=="FoulBallNF"):
                        pdf.regular_polygon(pdf.get_x()+width-3,pdf.get_y()-height+3,polyWidth=6,rotateDegrees=198,numSides=5,style='FD')
                    pdf.text(pdf.get_x()+width-1 if (i+1)<10 else pdf.get_x()+width-2,pdf.get_y()-height+1,str(i+1))
                    #print(pdf.x,pdf.y)
                    #pdf.set_xy(FourSliceOriginArray[ABFours][0],FourSliceOriginArray[ABFours][1])
                    #pdf.cell(pdf.get_x()+width,pdf.get_y()-height,str(i),False,ln=False)
                    
                
                ABFours+=1
                ABIndexCounter+=1
                PACount-=1
                CurAB+=1
                if(ABIndexCounter>=len(ABData)):
                   break

    print("Done")
    if outputname_batter!="":
        pdf.output(outputname_batter)

print("Generator Imported")
#if __name__=="__main__":
    #baseballstring = sys.argv[1]
    #genStats(baseballstring)
