
<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
   <v-flex xs12 >
	<v-progress-linear v-model="valueDeterminate"></v-progress-linear>
  </v-flex>
  <v-flex xs12>
	  <fieldset>
      		<input type="text" placeholder="Your answer" @focus="show" data-layout="compact" />
	  </fieldset>
  </v-flex>
   <v-flex xs12 v-if="!visible">
    <v-btn color="info" @click="lower_level()">Before</v-btn>
    <v-btn @click="solve_answer()" color="success">Solve</v-btn>
    <v-btn @click="read_text()" color="info">Play Me</v-btn>
    <v-btn color="info" @click="add_level()">Next</v-btn>
  </v-flex>
  <v-flex xs12>
    <vue-touch-keyboard :options="options" v-if="visible" :layout="layout" :cancel="hide" :accept="accept" :input="input" />
  </v-flex>
  <div>
  </div>

    </v-layout>
  </v-container>
</template>

<script>
  export default {
	data: () => ({
		max_questions:6,
		current_question:0,
		current_level:0,
		valueDeterminate:0,
		visible: false,
	      	layout: "normal",
	      	input: null,
	      	options: {
			useKbEvents: false,
			preventClickEvent: false}
	}),
	
	created: function(){
		this.reload_state()
	},
	
	methods: {
	accept(text) {
		this.input=text;
          	this.hide();
        },

        show(e) {
          this.input = e.target;
          this.layout = e.target.dataset.layout;

          if (!this.visible)
            this.visible = true
        },

        hide() {
          this.visible = false;
        },

	reload_state:function(){
		this.axios.get("http://"+window.location.hostname+":"+window.location.port+"/api/state").then(response => (this.update_state(response)))
	},

	update_state:function(response){
		console.log(response)
		this.max_questions = response.data.num_levels-1
		this.current_level = response.data.max_level
	},
	
	solve_answer:function(){
		alert(window.location.hostname)
		console.log(window.location.hostname);
		this.axios.get("http://"+window.location.hostname+":"+window.location.port+"/api/solve/"+this.current_question+"/"+this.input).then(
		this.reload_state())
	},

	read_text:function(){
		this.axios.get("http://"+window.location.hostname+":"+window.location.port+"/api/level/"+this.current_question)
	},

	delete_number: function(){
		this.answer=[]
	},

	recalc_status: function(){
		this.valueDeterminate = 100/this.max_questions * this.current_question
	},

	add_level:function(){
		this.change_current(1)
	},

	lower_level:function(){
		this.change_current(-1)
	},

	change_current:function(changed){
		if(this.current_question+changed<=this.max_questions && this.current_question+changed>=0)
		{
			if(this.current_level >= this.current_question + changed){
				this.current_question+=changed;
			}
			this.recalc_status()
			//console.log(this.current_question)
		}
	}
}
  }
</script>

<style>
html {
	font-family: Tahoma;
	font-size: 12px;
}

#keyboard {
	position: fixed;
	left: 0;
	right: 0;
	bottom: 0;

	z-index: 1000;
	width: 100%;
	max-width: 1000px;
	margin: 0 auto;

	padding: 1em;

	background-color: #EEE;
	box-shadow: 0px -3px 10px rgba(black, 0.3);

	border-radius: 10px;
}

fieldset {
	display: block;
	width: 300px;
	padding: 15px;
	margin: 15px auto;
	border-style: solid;
	background-color: #fff;
	border-color: #ddd;
	border-width: 1px;
	border-radius: 4px;	
}

input {
	display: block;
	width: 100%;
	height: 34px;
	padding: 6px 12px;
	font-size: 14px;
	line-height: 1.42857143;
	color: #555;
	background-color: #fff;
	background-image: none;
	border: 1px solid #ccc;
	border-radius: 4px;
	box-shadow: inset 0 1px 1px rgba(0,0,0,.075);
	transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s;		

	&:focus {
		border-color: #66afe9;
		outline: 0;
		box-shadow: inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6);			
	}
}
</style>
