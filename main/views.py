# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from main.models import Story, EventNode, EvalNode, TransiDecorator, Transition

import json, urllib2
from threading import Timer
import random

# Create your views here.
class Personality:
    attr = {"intel" : 0, "health" : 0, "look" : 0}

    def clear(self):
        attr = self.attr
        attr["intel"] = random.randint(0,4)
        attr["health"] = random.randint(0,4)
        attr["look"] = random.randint(0,4)

class Mine:
    psn = Personality()
    stories = []
    result = []

    def electric_flag(self):

        #api_url = "http://escamp.ongetit.com/1.1/devices/:deviceId/realtime/usages/:timestamp"
        #data = urllib2.urlopen(api_url).read()
        return random.choice(["high","low","mid"])

    def transition_string(self, status, target):
        qs = Transition.objects.filter(aspect__iexact=target)
        if status == "high":
            qs = qs.filter(is_buff__exact=True)
            qs = qs.filter(initial__exact=self.psn.attr[target])
            deco = TransiDecorator.objects.filter(is_buff__exact=True)
        elif status == "mid":
            return ""
        else:
            qs = qs.filter(is_buff__exact=False)
            qs = qs.filter(initial__exact=self.psn.attr[target])
            deco = TransiDecorator.objects.filter(is_buff__exact=False)
        return random.choice(deco).content + " " + random.choice(qs).content

    def run_node_event(self,node_id):
        node = get_object_or_404(EventNode, pk=node_id)
        key = node.requirement
        score = self.psn.attr[key]

        if score > 2: #high
            return node.high
        elif score > 1:
            return node.mid
        else:
            return node.low

    def run_node_eval(self, node_id):
        node = get_object_or_404(EvalNode, pk=node_id)
        tgt = node.target
        status = self.electric_flag()
        if status == "high" and self.psn.attr[tgt]!=4:
            self.psn.attr[tgt] += 1
        elif status == "low" and self.psn.attr[tgt]!=0:
            self.psn.attr[tgt] -= 1
        return self.transition_string(status, tgt)

    def ref(self, request):
        temp = [] + self.result
        self.result = []
        return HttpResponse(json.dumps(temp), content_type="application/json")

    def run(self, request):
        self.result = []
        self.stories = []
        self.stories += Story.objects.all()
        self.psn.clear()
        self.build_first_msg()
        self.run_helper()
        return HttpResponse("Ok")

    def run_helper(self):
        if len(self.stories) == 0:
            self.build_last_msg()
            return
        else:
            Timer(2, self.run_helper, ()).start()
            story = self.stories.pop(0)
            temp = {}
            if story.is_event:
                temp["content"] = self.run_node_event(story.node_id)
                temp["isEvent"] = True
            else:
                temp["content"] = self.run_node_eval(story.node_id)
                if temp["content"] == "":
                    return
                temp["isEvent"] = False
            temp["health"] = self.psn.attr["health"]
            temp["look"] = self.psn.attr["look"]
            temp["intel"] = self.psn.attr["intel"]
            self.result.append(temp)

    def build_first_msg(self):
        health = self.psn.attr["health"]
        look = self.psn.attr["look"]
        intel = self.psn.attr["intel"]
        msg_0 = [u'매우 병약한 몸으로', u'병약한 몸으로', u'적당히 건강한 몸으로', u'건강한 몸으로', u'튼튼한 우량아로'][health]
        msg_1 = [u'열을 가르쳐주면 하나를 알았으며', u'다섯을 가르치면 하나를 알았으며', u'하나를 가르치면 하나를 알았으며', u'하나를 가르치면 열을 알았으며', u'가르치지 않아도 모든 것에 통달했으며'][intel]
        msg_2 = [u'이목구비를 구분할 수 없었다', u'자세히 보면 이목구비를 구분할 수 있었다', u'보통 사람이라면 이목구비를 구분할 수 있었다', u'이목구비가 적절한 위치에 있었다', u'이목구비가 서로 조화를 이루었다'][look]
        temp = {}
        temp["content"] = u'*는 %s 태어났다. %s, %s'%(msg_0, msg_1, msg_2)
        temp["isEvent"] = True
        temp["health"] = health
        temp["intel"] = intel
        temp["look"] = look
        self.result.append(temp)

    def build_last_msg(self):
        health = self.psn.attr["health"]
        look = self.psn.attr["look"]
        intel = self.psn.attr["intel"]
        msg = u'*는 %d세의 나이로 세상을 떠났다. 그 때에 *는 배우자가 %d명 슬하에 손자가 %d명이었다.'%(intel*5+80,look,health)
        if health == look and look == intel and intel == 4:
            msg = u'*는 우주 정복을 위해 태어난 사람이었다. 알에서 태어난 *는 태어나서부터 비범한 능력이 있었고 무예와 학업에 모두 뛰어난 성과를 보였다. 많은 사람들에게 존경을 받았으며 그가 이룬 위업은 인류의 역사에 길이길이 남을 것이다.'
        if health == look and look == intel and intel == 3:
            msg = u'*는 외계인이었다. 지구인과 비슷한 외모였던 *는 지구를 사랑해서 지구에 남았다. *가 외계인이라는 것을 알아보는 사람이 아무도 없어 *는 만족하며 숨을 거두었다.'
        if health == look and look == intel and intel == 2:
            msg = u'*는 평범한 사람이었다. 평범한 것이 특징인 사람이었는데 어떤 상황에서도 *는 평범한 범위에 속하는 사람이었다. 관심을 받고싶어하던 *는 평생 한 번도 주목받지 못한것을 한으로 삼았다.'
        if health == look and look == intel and intel == 1:
            msg = u'*는 고기를 굉장히 좋아했는데 고기라면 무슨 고기든 가리지 않고 잘 먹었다. *는 노년에 성인병에 시달렸다. *는 27명의 배우자와 수많은 아이를 두었는데 배우자들이 서로 싸우느라 그의 가정은 조용한 날이 없었다고 한다.'
        if health == look and look == intel and intel == 0:
            msg = u'*는 힘겨운 삶을 살았다. 평생 질병이 *를 따라다녔으며 노년에 배우자를 먼저 보내고 쓸쓸한 삶을 살았다. 자녀는 소문난 망나니로 항상 자녀때문에 속을 썩였고 본인의 일에 있어서도 큰 성공을 거두지 못했다.'
        temp = {}
        temp["content"] = msg
        temp["isEvent"] = True
        temp["health"] = health
        temp["intel"] = intel
        temp["look"] = look
        self.result.append(temp)
        return

mmm = Mine()
run = mmm.run
ref = mmm.ref

def index(request):
    return render(request, 'main/index.html', {})
