<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
   <v-flex xs12>
	<v-progress-linear v-model="valueDeterminate"></v-progress-linear>
          <div>
            <v-btn color="primary" fab small dark>
              {{answer[0]}}
            </v-btn>
            <v-btn color="primary" fab small dark>
              {{answer[1]}}
            </v-btn>
            <v-btn color="primary" fab small dark>
              {{answer[2]}}
            </v-btn>
            <v-btn color="primary" fab small dark>
              {{answer[3]}}
            </v-btn>
          </div>
  </v-flex>
   <v-flex xs12>
    <v-btn v-on:click="add_number(1)" color="info">1</v-btn>
    <v-btn v-on:click="add_number(2)" color="info">2</v-btn>
    <v-btn v-on:click="add_number(3)" color="info">3</v-btn>
  </v-flex>
   <v-flex xs12>
    <v-btn v-on:click="add_number(4)" color="info">4</v-btn>
    <v-btn v-on:click="add_number(5)" color="info">5</v-btn>
    <v-btn v-on:click="add_number(6)" color="info">6</v-btn>
  </v-flex>
   <v-flex xs12>
    <v-btn v-on:click="add_number(7)" color="info">7</v-btn>
    <v-btn v-on:click="add_number(8)" color="info">8</v-btn>
    <v-btn v-on:click="add_number(9)" color="info">9</v-btn>
  </v-flex>
   <v-flex xs12>
    <v-btn color="info" @click="lower_level()">Before</v-btn>
    <v-btn v-on:click="delete_number()" color="error">Retry</v-btn>
    <v-btn @click="solve_answer()" color="success">Solve</v-btn>
    <v-btn color="info" @click="add_level()">Next</v-btn>
  </v-flex>
   <v-flex xs12>
    <v-btn @click="read_text()" color="info">Play Me</v-btn>
  </v-flex>
  <p> {{max_questions}} </p>
  <p> {{current_question}} </p>
  <p> {{current_level}} </p>

    </v-layout>
  </v-container>
</template>

<script>
  export default {
	data: () => ({
		answer:[],
		max_questions:6,
		current_question:0,
		current_level:0,
		valueDeterminate:0
	}),
	
	created: function(){
		this.reload_state()
	},
	
	methods: {
		add_number: function(number_in){
			this.axios.get("http://"+window.location.hostname+"/api/number/"+number_in)
			if (this.answer.length < 5){
				this.answer.push(number_in)
			}
	},

	reload_state:function(){
		this.axios.get("http://"+window.location.hostname+"/api/state").then(response => (this.update_state(response)))
	},

	update_state:function(response){
		console.log(response)
		this.max_questions = response.data.num_levels-1
		this.current_level = response.data.max_level
	},
	
	solve_answer:function(){
		console.log(window.location.hostname);
		this.axios.get("http://"+window.location.hostname+"/api/solve/"+this.current_question+"/"+this.answer.join("")).then(
		this.reload_state())
	},

	read_text:function(){
		this.axios.get("http://"+window.location.hostname+"/api/level/"+this.current_question)
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

</style>
