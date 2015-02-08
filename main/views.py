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
        attr["intel"] = 0
        attr["health"] = 0
        attr["look"] = 0

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
        self.run_helper()
        return HttpResponse("Ok")

    def run_helper(self):
        if len(self.stories) == 0:
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

mmm = Mine()
run = mmm.run
ref = mmm.ref
